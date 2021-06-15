def filter_by_extension(data: dict, extensions: list) -> dict:
    """
    Return filtered data by extensions
    :param data, extensions:
    :return: data:
    :rtype: dict:
    """
    del_keys = []
    for key, values in data.items():
        ext_files = []
        for value in values:
            if isinstance(value, dict):
                res = filter_by_extension(value, extensions=extensions)
                for k, v in value.items():
                    ext_files.append(res)
            else:
                cnt = 0
                for ext in extensions:
                    if value.endswith(ext):
                        cnt += 1
                        ext_files.append(value)
        values = ext_files
        if ext_files == []:
            del_keys.append(key)
        else:
            data[key] = values
    for key in del_keys:
        del data[key]

    return data


def get_repo_content_path(data: dict):
    """
    Return all content path
    :param data:
    :return: list of all paths:
    :rtype: list:
    """
    paths = []
    for key in data.keys():
        for file in data[key]:
            if isinstance(file, dict):
                for k, v in file.items():
                    s = get_repo_content_path(file)
                    for item in s:
                        path = k + '/' + item
                        paths.append(path)
            else:
                path = file
                paths.append(path)
    return paths
