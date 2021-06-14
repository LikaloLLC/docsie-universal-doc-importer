def filter_by_extension(data, extensions):
    del_keys = []
    for key, values in data.items():
        lst = []
        for value in values:
            if isinstance(value, dict):
                res = filter_by_extension(value, extensions=extensions)
                for k, v in value.items():
                    lst.append(res)
            else:
                cnt = 0
                for ext in extensions:
                    if value.endswith(ext):
                        cnt += 1
                        lst.append(value)
        values = lst
        if lst == []:
            del_keys.append(key)
        else:
            data[key] = values
    for key in del_keys:
        del data[key]

    return data
