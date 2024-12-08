# Copyright 2023-2025 Huawei Technologies Co., Ltd
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
Generate operator utils function
"""
import os
import glob
import hashlib
import pathlib
import re
import stat
import yaml


def convert_dtype_str(dtype_str):
    """
    Convert dtype str to expression in ops file
    """
    return 'DT_' + dtype_str.replace('[', '_').replace(']', '').upper()


def get_type_str(type_str):
    """
    Get the unified type str for operator arg dtype.
    """
    # add more type here
    type_kind_set = {
        'int',
        'float',
        'bool',
        'number',
        'tuple[int]',
        'tuple[float]',
        'tuple[bool]',
        'tuple[tensor]',
        'tuple[str]',
        'list[int]',
        'list[float]',
        'list[bool]',
        'list[tensor]',
        'list[str]',
        'tensor',
        'type',
    }
    if type_str in type_kind_set:
        return "OpDtype." + convert_dtype_str(type_str)
    raise TypeError(f"""Unsupported type {type_str} for args.""")


def get_file_md5(file_path):
    """
    Get the md5 value for file.
    """
    if not os.path.exists(file_path):
        return ""
    if os.path.isdir(file_path):
        return ""
    with open(file_path, 'rb') as f:
        data = f.read()
    md5_value = hashlib.md5(data).hexdigest()
    return md5_value


def check_change_and_replace_file(last_file_path, tmp_file_path):
    """
    Compare tmp_file with the md5 value of the last generated file.
    If the md5 value is the same, retain the last generated file.
    Otherwise, update the last generated file to tmp_file.
    """
    last_md5 = get_file_md5(last_file_path)
    tmp_md5 = get_file_md5(tmp_file_path)

    if last_md5 == tmp_md5:
        os.remove(tmp_file_path)
    else:
        if os.path.exists(last_file_path):
            os.remove(last_file_path)
        os.rename(tmp_file_path, last_file_path)


def merge_files_to_one_file(file_paths, merged_file_path):
    """
    Merge multiple files into one file.
    """
    merged_content = ''
    file_paths.sort()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            merged_content += file.read()
            merged_content += '\n'
    with open(merged_file_path, 'w') as file:
        file.write(merged_content)


def merge_files(origin_dir, merged_file_path, file_format):
    """
    Merge multiple files into one file.
    origin_dir: indicates the origin file directory.
    merged_file_path: indicates the merged file path.
    file_format: indicates the format of regular matching.
    Files whose names meet the regular matching in 'origin_dir' directory will be merged into one file.
    """
    op_yaml_file_names = glob.glob(os.path.join(origin_dir, file_format))
    merge_files_to_one_file(op_yaml_file_names, merged_file_path)


def merge_files_append(origin_dir, merged_file_path, file_format):
    """
    Merge multiple files into one file.
    origin_dir: indicates the origin file directory.
    merged_file_path: indicates the merged file path.
    file_format: indicates the format of regular matching.
    Files whose names meet the regular matching in 'origin_dir' directory will be merged into one file.
    """
    file_paths = glob.glob(os.path.join(origin_dir, file_format))
    merged_content = ''
    file_paths.sort()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            merged_content += file.read()
            merged_content += '\n'
    with open(merged_file_path, 'a') as file:
        file.write(merged_content)


def safe_load_yaml(yaml_file_path):
    """
    Load yaml dictionary from file.
    """
    yaml_str = dict()
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_str.update(yaml.safe_load(yaml_file))
    return yaml_str


def get_assign_str_by_type_it(class_name, arg_info, arg_name, dtype):
    """
    Make type_it(arg, src_types, dst_type) python sentences.
    """
    assign_str = ""
    type_cast = arg_info.get('type_cast')
    if type_cast is not None:
        type_cast_tuple = tuple(ct.strip() for ct in type_cast.split(","))
        assign_str += f"type_it('{class_name}', '{arg_name}', {arg_name}, "
        if len(type_cast_tuple) == 1:
            assign_str += get_type_str(type_cast_tuple[0]) + ', '
        else:
            assign_str += '(' + ', '.join(get_type_str(ct) for ct in type_cast_tuple) + '), '
        assign_str += get_type_str(dtype) + ')'
    else:
        assign_str = arg_name
    return assign_str


def write_file(path, data):
    """
    write data to path
    :param path:
    :param data:
    :return:
    """
    flags = os.O_RDWR | os.O_CREAT
    mode = stat.S_IWUSR | stat.S_IRUSR
    fd = os.open(path, flags, mode)
    with os.fdopen(fd, "w") as f:
        f.write(data)


def save_file(save_path, file_name, content):
    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
    dst_file_path = os.path.join(save_path, file_name)
    tmp_file_path = os.path.join(save_path, f"tmp_{file_name}")
    write_file(tmp_file_path, content)
    check_change_and_replace_file(dst_file_path, tmp_file_path)


def normalize_func_description_format(description):
    """
    Process description.
    """
    if not description:
        return description
    lines = description.split("\n")
    if len(lines) == 1:
        return description

    # Add line indentation to other lines after the first line
    for i in range(1, len(lines)):
        indent = "    " if lines[i] else ""
        lines[i] = indent + lines[i]

    # Remove trailing blank lines
    lines = lines if lines[-1] != "" else lines[:-1]
    description = "\n".join(lines)
    return description


def get_op_description(operator_name, doc_dict):
    """
    Generate ops api description.
    """
    op_description = f"    r\"\"\"\n" \
                     f"    \n" \
                     f"    \"\"\"\n"
    if doc_dict is None:
        print(f"Description is None, op_name: {operator_name}")
        return op_description

    description = doc_dict.get(operator_name)
    if description is None:
        print(f"Description is None, op_name: {operator_name}")
        return op_description

    description = description.get("description")
    if description is None:
        print(f"Description is None, op_name: {operator_name}")
        return op_description

    op_description = f"    r\"\"\"\n" \
                     f"    {normalize_func_description_format(description)}\n" \
                     f"    \"\"\"\n"
    return op_description


def get_same_dtype_groups(args_signature, args_name):
    """
    Get same dtype groups
    """
    same_dtype_groups = {}
    dtype_count = 0

    if not args_signature:
        return same_dtype_groups, dtype_count

    dtype_group = args_signature.dtype_group
    if not args_signature.dtype_group:
        return same_dtype_groups, dtype_count

    args_list = []
    match = re.findall(r'\((.*?)\)', dtype_group)
    for item in match:
        args_list.append(item.replace(' ', '').split(","))
    for arg_name in args_name:
        if arg_name in same_dtype_groups:
            continue
        is_match = False
        for group in args_list:
            if arg_name in group:
                is_match = True
                for item in group:
                    same_dtype_groups[item] = dtype_count
                break
        if not is_match:
            same_dtype_groups[arg_name] = dtype_count
        dtype_count = dtype_count + 1
    return same_dtype_groups, dtype_count


def init_args_signature_rw(args_signature):
    """
    Extracts read, write, and reference argument lists from signature data.

    Args:
        args_signature (object): Contains 'rw_write', 'rw_read', 'rw_ref' attributes as comma-separated strings.

    Returns:
        tuple: Lists of read-only, reference, and write-only argument names.
    """
    write_list = []
    read_list = []
    ref_list = []
    if args_signature:
        if args_signature.rw_write:
            write_list.extend(args_signature.rw_write.replace(' ', '').split(","))

        if args_signature.rw_read:
            read_list.extend(args_signature.rw_read.replace(' ', '').split(","))

        if args_signature.rw_ref:
            ref_list.extend(args_signature.rw_ref.replace(' ', '').split(","))

    return read_list, ref_list, write_list
