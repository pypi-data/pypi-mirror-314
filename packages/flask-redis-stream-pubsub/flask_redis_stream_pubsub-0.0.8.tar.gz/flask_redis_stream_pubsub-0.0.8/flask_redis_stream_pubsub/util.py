def chunk_array(arr, size):
    return [arr[i:i + size] for i in range(0, len(arr), size)]


def split_dict(input_dict, num_parts):
    # 计算字典的长度
    total_length = len(input_dict)

    # 计算每份的大小
    part_size = total_length // num_parts
    remainder = total_length % num_parts

    # 分割字典
    keys = list(input_dict.keys())
    result = []
    start_index = 0

    for i in range(num_parts):
        # 计算当前部分的大小
        current_part_size = part_size + (1 if i < remainder else 0)
        end_index = start_index + current_part_size

        # 创建当前部分的字典
        current_dict = {key: input_dict[key] for key in keys[start_index:end_index]}
        if current_dict:
            result.append(current_dict)

        # 更新起始索引
        start_index = end_index

    return result