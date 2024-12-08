# Copyright 2024 Huawei Technologies Co., Ltd
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
"""
Generates mindspore/common/_tensor_docs.py that attaches docs to tensor func APIs when import mindspore
"""

import os
import gen_constants as K
from gen_utils import save_file
import template
from template import Template
from base_generator import BaseGenerator


class AddTensorDocsGenerator(BaseGenerator):
    """
    This class is responsible for generating a helper file that enable users to view the docstrings of Tensor func APIs.
    """

    def __init__(self):
        self.ADD_TENSOR_DOCS_TEMPLATE = template.ADD_TENSOR_DOCS_TEMPLATE
        self.attach_single_docstr_template = Template('attach_docstr("${api_name}", r"""${docstr}""")')

    def generate(self, work_path, tensor_docs_data):
        """
        Generates the content for the helper file and saves it to the specified path.

        Args:
            work_path (str): The directory where the generated file will be saved.
            tensor_docs_data (dict): A dict mapping from Tensor func API names to their docstrings.

        Returns:
            None
        """
        add_doc_statements = []
        for api_name, tensor_doc in tensor_docs_data.items():
            single_add_doc_statement = self.attach_single_docstr_template.replace(api_name=api_name,
                                                                                  docstr=tensor_doc['description'])
            single_add_doc_statement += template.NEW_LINE
            add_doc_statements.append(single_add_doc_statement)
        _tensor_docs_py_str = self.ADD_TENSOR_DOCS_TEMPLATE.replace(add_doc_statements=add_doc_statements)
        save_file(os.path.join(work_path, K.ADD_TENSOR_DOCS_PY_PATH), "_tensor_docs.py", _tensor_docs_py_str)
