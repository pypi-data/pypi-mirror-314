def chunks(input_data, sizes:int|list|tuple, reverse=False,append_last=True):
    """
    Splits a list or dictionary into sublists/subdicts based on the specified sizes.

    :param input_data: The list or dictionary to be split
    :param sizes: A tuple or list of integers representing the sizes of the sublists/subdicts
    :param reverse: If True, reverses each chunk
    :param append_last: If True, appends remaining elements as last chunk
    :return: A list of sublists/subdicts split according to the sizes
    """
    do_reverse = lambda x: x[::-1] if reverse else x
    
    # Handle dictionary input
    if isinstance(input_data, dict):
        items = list(input_data.items())
        chunks_result = chunks(items, sizes, reverse, append_last)
        return [dict(chunk) for chunk in chunks_result]
    
    # Original list handling
    if isinstance(sizes, int):
        res = []
        for i in range(0, len(input_data), sizes):
            res += [do_reverse(input_data[i:i + sizes])]
        return res
        
    result = []
    start_index = 0

    for size in sizes:
        end_index = start_index + size
        result.append(do_reverse(input_data[start_index:end_index]))
        start_index = end_index
    if append_last and start_index < len(input_data):
        result.append(do_reverse(input_data[start_index:]))

    return result


import collections
def sort_dict_by_key(item:dict,reverse=False):
    return dict(collections.OrderedDict(sorted(item.items(),reverse=reverse)))

def sort_dict_by_val(item:dict,reverse=False):
    sorted_x = sorted(item.items(), key=lambda kv: kv[1],reverse=reverse)
    return dict(collections.OrderedDict(sorted_x))
