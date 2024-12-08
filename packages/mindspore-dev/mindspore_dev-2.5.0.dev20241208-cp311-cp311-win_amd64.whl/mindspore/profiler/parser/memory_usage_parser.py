# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Memory Usage Parser."""
from collections import OrderedDict

from mindspore import log as logger
from mindspore.profiler.parser.container import MemoryGraph as Graph
from mindspore.profiler.parser.container import MemoryNode as Node
from mindspore.profiler.parser.container import MemoryTensor as Tensor

GIGABYTES = 1024 * 1024 * 1024


class GraphMemoryParser:
    """Parse memory usage data for each graph."""

    def __init__(self, graph_proto, points, framework):
        self.graph = None
        self.nodes = OrderedDict()
        self.tensors = OrderedDict()
        self._framework = framework
        self._points = points
        self._graph_proto = graph_proto
        self.peak_mem = 0
        self.static_mem = 0
        self.allocations = 0
        self.deallocations = 0
        self.node_sampling_num = 2000
        self.tensor_node_id = 0
        self.sampling_step = 1
        self._mem_change = []
        self.breakdowns = []
        self._lifetime = []
        # compatible with original mode
        self._multi_graph = False
        if not isinstance(self._points, dict):
            raise TypeError("Input points data must be dict!")
        if not self._points.get("fp_start"):
            self._multi_graph = True

    @staticmethod
    def _remove_duplicate_tensors(node):
        """Find conflict tensors in node."""
        if node.workspace_ids:
            i = 0
            while i < len(node.workspace_ids):
                t_id = node.workspace_ids[i]
                if t_id in node.output_ids:
                    del node.workspace_ids[i]  # remove duplicate tensor
                    continue
                i += 1

    @staticmethod
    def _get_tensor_dict(node, tensor, t_id):
        """Update node outputs to assemble memory breakdowns."""
        for i, output_id in enumerate(node.output_ids):
            if t_id == output_id:
                output = node.outputs[i] if i < len(node.outputs) else {}
                tensor.name = node.name + ':' + str(i)
                tensor.shape = output.get('shape')
                tensor.dtype = output.get('data_type')
                tensor.format = output.get('format')
                tensor.type = 'output'

        return tensor.to_dict()

    def parse_graph(self):
        """Parse memory usage data for subgraphs."""
        graph_dict = {}
        model_id = -1
        self.graph = Graph(self._graph_proto)
        # process tensors in the graph
        tensors_proto = self._graph_proto.tensor_mems
        if not tensors_proto:
            logger.info('No tensor in graph %s, skipped.', self.graph.graph_id)
            return graph_dict, model_id
        self._parse_tensors(tensors_proto)

        # calculate memory usage of the graph by number of nodes and details of tensors
        nodes_proto = self._graph_proto.node_mems
        node_num = len(nodes_proto)
        # init memory usage list with static memory
        self._mem_change = [self.graph.static_mem for _ in range(node_num)]
        self._lifetime = [[] for _ in range(node_num)]
        self._calc_mem_change()  # update self._mem_change and self._lifetime

        # To prevent large memory data, sample the memory.
        self.sampling_step = node_num // self.node_sampling_num
        if node_num > self.node_sampling_num:
            self.graph.lines = self._mem_change[::self.sampling_step]
        else:
            self.graph.lines = self._mem_change

        # process nodes in graph
        self.graph.nodes = self._parse_nodes(nodes_proto)

        self._process_memory_breakdowns()
        self.graph.breakdowns = [self.breakdowns[self.tensor_node_id]]

        # update fp_start and bp_end
        point_id, model_id = self._locate_fp_bp_id()
        self.graph.fp_start = point_id.get('fp_start')
        self.graph.bp_end = point_id.get('bp_end')

        graph_dict = self.graph.to_dict()

        self.static_mem = self.graph.static_mem
        self.allocations = len(self.tensors)
        self.deallocations = len(self.tensors)
        self.peak_mem = max(max(self._mem_change), self.peak_mem)

        return graph_dict, model_id

    def _parse_tensors(self, tensors_proto):
        """Parse tensors."""
        for tensor_proto in tensors_proto:
            tensor = Tensor(tensor_proto)
            self.tensors.update({tensor.tensor_id: tensor})

    def _parse_nodes(self, nodes_proto):
        """Parse nodes."""
        nodes_list = []
        for index, node_proto in enumerate(nodes_proto):
            node = Node(node_proto)
            # Calculate memory size allocated for this node
            tensor_ids = set(node.output_ids + node.workspace_ids)
            node.size = self._calc_node_memory(tensor_ids)
            node.allocations = len(tensor_ids)
            node.deallocations = len(tensor_ids)

            # calculate the allocated/deallocated memory size on the node
            if index == 0:
                node.mem_change = self._mem_change[index] - self.graph.static_mem
            else:
                node.mem_change = self._mem_change[index] - self._mem_change[index - 1]

            self._update_nodes(node)
            self._update_tensor_source(node)
            self.nodes[node.name] = node
            nodes_list.append(node.to_dict())
            node_num = index + 1

        # To prevent large memory data, sample the memory.
        if node_num > self.node_sampling_num:
            return nodes_list[::self.sampling_step]
        return nodes_list

    def _update_nodes(self, node):
        """Update nodes."""
        # Remove duplicate tensors
        self._remove_duplicate_tensors(node)
        name = node.name
        if self._framework and name in self._framework:
            node_frame = self._framework[name]
            node.fullname = node_frame.get('fullname')
            info = node_frame.get('args')
            for key, value in info.items():
                if 'input' in key:
                    node.inputs.append(value)
                else:
                    node.outputs.append(value)

    def _update_tensor_source(self, node):
        """Update source node for tensors."""
        for t_id in node.output_ids:
            tensor = self.tensors.get(t_id)
            tensor.source_node = node.name

    def _calc_node_memory(self, tensor_ids):
        """Calculate the allocated memory for the node."""
        node_mem = 0
        for t_id in tensor_ids:
            tensor = self.tensors[t_id]
            size = tensor.size
            node_mem += size

        return node_mem

    def _calc_mem_change(self):
        """Calculate the memory change for the subgraph."""
        node_num = len(self._mem_change)
        for tensor_id, tensor in self.tensors.items():
            life_long = tensor.life_long
            life_start = tensor.life_start
            life_end = tensor.life_end
            size = tensor.size

            # Update memory change for the entire graph.
            # If a tensor's lifetime cannot be fully located, it will be ignored as 0 change.
            if life_long == 'LifeLongGraphAll':  # lifetime is from graph start to graph end
                tensor.life_start = 0
                tensor.life_end = node_num
                self._update_mem_change(size, 0, node_num, tensor_id)
            elif life_long == 'LifeLongGraphStart':  # lifetime is from graph start to tensor end
                if life_end is not None and life_end >= 0:
                    tensor.life_start = 0
                    self._update_mem_change(size, 0, life_end + 1, tensor_id)
                else:
                    logger.info('Cannot locate lifetime end for tensor: %s', tensor_id)
            elif life_long == 'LifeLongGraphEnd':  # lifetime is from tensor start to graph end
                if life_start is not None and life_start <= node_num:
                    tensor.life_end = node_num
                    self._update_mem_change(size, life_start, node_num, tensor_id)
                else:
                    logger.info('Cannot locate lifetime start for tensor: %s', tensor_id)
            elif life_long == 'LifeLongNone':  # lifetime is from tensor start to tensor end
                if life_start is not None and life_end is not None and life_start <= life_end:
                    self._update_mem_change(size, life_start, life_end + 1, tensor_id)
                else:
                    logger.info('Cannot locate lifetime start or end for tensor: %s', tensor_id)

    def _update_mem_change(self, size, start, end, tensor_id):
        """Update memory change for the subgraph."""
        for i in range(start, end):
            self._mem_change[i] += size
            # Update tensor lifetime list.
            self._lifetime[i].append(tensor_id)

    def _locate_fp_bp_id(self):
        """Locate the node id of fp_start and bp_end in graph."""
        model_id = 0
        if not self._multi_graph:
            point_id = self._match_graph_fpbp(self._points)
        else:
            for mod_id, points in self._points.items():
                if not isinstance(points, dict) or not mod_id.startswith("model"):
                    raise RuntimeError("Inputs points is invalid!")
                point_id = self._match_graph_fpbp(points)
                if point_id.get("fp_start"):
                    model_id = int(mod_id.split("_")[-1])
                    break
        if not point_id.get("fp_start") or not point_id.get("bp_end"):
            model_id = -1

        return point_id, model_id

    def _match_graph_fpbp(self, points):
        "Match model_id and graph_id"
        point_id = {
            'fp_start': None,
            'bp_end': None
        }
        fp_start = points.get('fp_start')
        bp_end = points.get('bp_end')
        fp_name = fp_start.split('/')[-1] if fp_start else ""
        bp_name = bp_end.split('/')[-1] if bp_end else ""
        if fp_name in self.nodes:
            point_id['fp_start'] = self.nodes[fp_name].node_id
        if bp_name in self.nodes:
            point_id['bp_end'] = self.nodes[bp_name].node_id

        return point_id

    def _process_memory_breakdowns(self):
        """Process memory breakdowns for each node."""
        self.breakdowns = [[] for _ in range(len(self._lifetime))]
        for index, breakdown in enumerate(self._lifetime):
            for t_id in breakdown:
                tensor = self.tensors.get(t_id)
                source_node = tensor.source_node
                if not source_node:
                    continue
                node = self.nodes.get(source_node)
                tensor_dict = self._get_tensor_dict(node, tensor, t_id)
                self.breakdowns[index].append(tensor_dict)
