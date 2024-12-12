import os
import json
import random
import openpyxl

def print_success():
    print("easytool 版本：0.1.6")

# tool
def add_size_4_filepath(filepath, size):
    _filepath, suffix =  filepath.split('.')[:-1], filepath.split('.')[-1]
    filepath = '.'.join(_filepath) + f"_{size}" + f".{suffix}"
    return filepath

# 文件读取
## json, jsonl
def load_json(filepath, **kwargs):
    data = list()
    with open(filepath, "rt", encoding="utf-8") as fin:
        data = json.load(fin, **kwargs)
    return data

def load_jsonlines(filepath, **kwargs):
    data = list()
    with open(filepath, "rt", encoding="utf-8") as fin:
        for idx, line in enumerate(fin):
            line_data = json.loads(line.strip())
            data.append(line_data)
    return data

def load_json_or_jsonl(filepath):
    try:
        data_list = load_json(filepath)
    except :
        data_list = load_jsonlines(filepath)
    return data_list

def load_jsonfile_list(filepath_list):
    all_json_data_list = []
    for filepath in filepath_list:
        all_json_data_list.extend(load_json_or_jsonl(filepath=filepath))
    return all_json_data_list

## txt, log, and more...
def load_lines(filepath, split_by_line=False, combine_to_one=False):
    with open(filepath, 'r', encoding='utf-8') as fr:
        all_lines = fr.readlines()

    if split_by_line:
        return [line.strip() for line in all_lines]
    if combine_to_one:
        return ''.join(all_lines)
    return all_lines

def load_linefile_list(filepath_list, **kwargs):
    all_data_list = []
    for filepath in filepath_list:
        one_file_data = load_lines(filepath=filepath, **kwargs)
        all_data_list.extend(one_file_data)
    return all_data_list



# 文件写入
## json, jsonl
def dump_json(obj, filepath):
    with open(filepath, "wt", encoding="utf-8") as fout:
        json.dump(obj, fout, ensure_ascii=False, indent=4)

def dump_jsonlines(obj, filepath, **kwargs):
    with open(filepath, "wt", encoding="utf-8") as fout:
        for d in obj:
            line_d = json.dumps(
                d, ensure_ascii=False, **kwargs
            )
            fout.write("{}\n".format(line_d))

def dump_json_or_jsonl_with_size(obj, filepath, out_type='json', with_size=True):
    if with_size:
        filepath = add_size_4_filepath(filepath, len(obj))

    if out_type == 'json':
        dump_json(obj, filepath)
    else:
        dump_jsonlines(obj, filepath)

def dump_jsonlines_append(obj, filepath, **kwargs):
    with open(filepath, "a", encoding="utf-8") as fout:
        for d in obj:
            line_d = json.dumps(
                d, ensure_ascii=False, **kwargs
            )
            fout.write("{}\n".format(line_d))

# txt, log, and more...
def dump_lines(obj_list, filepath, with_size=True):
    if with_size:
        filepath = add_size_4_filepath(filepath, len(obj_list))

    with open(filepath, "wt", encoding="utf-8") as fout:
        for obj in obj_list:
            fout.write(str(obj) + '\n')

# excel
def read_excel_to_dict(file_path, sheet_name):
    # 加载 Excel 文件
    workbook = openpyxl.load_workbook(file_path)
    # 选择工作表
    sheet = workbook[sheet_name]
    # 获取表头
    headers = [cell.value for cell in sheet[1]]  # 第一行作为表头
    # 初始化字典列表
    data = []
    # 读取每一行数据
    for row in sheet.iter_rows(min_row=2, values_only=True):  # 从第二行开始
        row_data = {headers[i]: row[i] for i in range(len(headers))}
        data.append(row_data)
    return data


# 文件夹操作
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def file_exists(file_path):
    return os.path.isfile(file_path)

def ensure_directory_exists(file_path):
    # Check if the directory exists
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
        # Create the directory if it does not exist
        os.makedirs(directory_path)

# 文件分割
def devide_json_file(input_file, output_file_1, output_file_2, split_ratio=0.5, shuffle=True, **kwargs):
    all_data_list = load_json_or_jsonl(input_file)
    if shuffle:
        random.shuffle(all_data_list)
    
    split_point = int(len(all_data_list) * split_ratio)
    
    dump_json_or_jsonl_with_size(all_data_list[:split_point], output_file_1, **kwargs)
    dump_json_or_jsonl_with_size(all_data_list[split_point:], output_file_2, **kwargs)

# 文件转换与合并
def jsonl_2_json(input_filepath, output_filepath, **kwargs):
    json_obj_data = load_jsonlines(input_filepath)
    dump_json_or_jsonl_with_size(json_obj_data, output_filepath, out_type='json', **kwargs)

def json_2_jsonl(input_filepath, output_filepath, **kwargs):
    json_obj_data = load_json(input_filepath)
    dump_json_or_jsonl_with_size(json_obj_data, output_filepath, out_type='jsonl', **kwargs)

def combine_json_to_one_file(filepath_list, output_path):
    all_data_list = load_jsonfile_list(filepath_list)
    dump_json_or_jsonl_with_size(all_data_list, output_path)

def combine_lines_to_one_file(filepath_list, output_path):
    all_data_list = load_linefile_list(filepath_list, split_by_line=True)
    dump_lines(all_data_list, output_path)

# 文件格式修正
def modify_error_jsonl(input_filepath, output_filepath, split_string='"}', **kwargs):
    ## 修正因为“格式化文档”导致错乱的jsonl文件
    all_lines = load_lines(input_filepath)
    all_lines = [line.strip() for line in all_lines]
    all_content = ''.join(all_lines)

    json_string_list = list(filter(lambda x: len(x)>0, all_content.split(split_string)))
    json_obj_list = [eval(item+split_string) for item in json_string_list if len(item)>0]

    dump_json_or_jsonl_with_size(json_obj_list, output_filepath, **kwargs)


if __name__ == "__main__":
    pass