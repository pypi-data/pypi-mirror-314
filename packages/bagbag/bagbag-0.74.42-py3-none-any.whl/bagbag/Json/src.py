import json
import io
import os
import html_to_json
import demjson3

#print("load json")

def Dumps(obj, indent=4, ensure_ascii=False) -> str:
    """
    It takes a Python object and returns a JSON string
    
    :param obj: The object to be serialized
    :param indent: This is the number of spaces to indent for each level. If it is None, that
    will insert newlines but won't indent the new lines, defaults to 4 (optional)
    :param ensure_ascii: If True, all non-ASCII characters in the output are escaped with \\uXXXX
    sequences, and the result is a str instance consisting of ASCII characters only. If False, some
    chunks written to fp may be unicode instances. This usually happens because the input contains
    unicode strings or the, defaults to False (optional)
    :return: A string
    """
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii)

def Loads(s:str|io.TextIOWrapper) -> list | dict:
    """
    The function Loads can load JSON or HTML data from 
    1. a file (file path)
    2. a string
    3. a file object
    
    :param s: The parameter `s` can be either a string or a file object (`io.TextIOWrapper`). It
    represents the JSON data or HTML data that needs to be loaded
    :type s: str|io.TextIOWrapper
    :return: The function `Loads` returns a list or a dictionary depending on the input provided. If the
    input is a file object of type `io.TextIOWrapper`, it reads the contents of the file and returns a
    dictionary or a list after parsing the JSON data. If the input is a string, it checks if the string
    starts with `[` or `{` and returns a dictionary or a list after
    """
    if type(s) == io.TextIOWrapper:
        return demjson3.decode(s.read())
    
    if type(s) == str:
        if s.startswith('[') or s.startswith('{'):
            return demjson3.decode(s)
        elif os.path.exists(s):
            data = open(s).read()
            try:
                return demjson3.decode(data)
            except:
                return html_to_json.convert(data)
        else:
            return html_to_json.convert(s)

def Valid(json_string:str) -> bool:
    """
    检查一个 JSON 字符串是否合法

    参数:
        json_string (str): 要检查的 JSON 字符串

    返回:
        bool: 如果 JSON 字符串合法则返回 True，否则返回 False
    """
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False

def ExtraValueByKey(obj:list|dict, key:str) -> list:
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)

                if k == key:
                    arr.append(v)
                    
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def DeleteKeyContainString(obj:list|dict, target_string:str) -> dict|list:
    """
    遍历字典并删除包含特定字符串的键值对

    参数:
    d (dict): 需要遍历的字典
    target_string (str): 需要查找的字符串

    返回:
    dict: 删除包含目标字符串的键值对后的字典
    """
    keys_to_delete = [key for key in obj if target_string in key]

    for key in keys_to_delete:
        del obj[key]

    for key, value in obj.items():
        if isinstance(value, dict):
            DeleteKeyContainString(value, target_string)

    return obj

def DeleteKeyMatchString(obj:list|dict, target_string:str) -> dict|list:
    """
    遍历字典并删除等于特定字符串的键值对

    参数:
    d (dict): 需要遍历的字典
    target_string (str): 需要查找的字符串

    返回:
    dict: 删除等于目标字符串的键值对后的字典
    """
    keys_to_delete = [key for key in obj if target_string == key]

    for key in keys_to_delete:
        del obj[key]

    for key, value in obj.items():
        if isinstance(value, dict):
            DeleteKeyContainString(value, target_string)

    return obj

if __name__ == "__main__":
    # j = Dumps({1: 3, 4: 5})
    # print(j)

    # d = Loads(j)
    # print(d)

    # print(type(d))

    # ------------

    # data = {
    #     "key": {
    #         "key": [
    #             {
    #                 "a": "b"
    #             },
    #             {
    #                 "key": "123"
    #             }
    #         ]
    #     }
    # }

    # print(ExtraValueByKey(data, "key"))

    html_string = """<head>
    <title>Test site</title>
    <meta charset="UTF-8"></head>"""

    print(Loads(html_string))