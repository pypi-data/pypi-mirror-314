import json


def dict2json(dict_data, ensure_ascii=False, indent=2):
	json_str = json.dumps(dict_data, ensure_ascii=ensure_ascii, indent=indent)
	return json_str


def json2dict(json_str):
    dict_data = json.loads(json_str)
    return dict_data
