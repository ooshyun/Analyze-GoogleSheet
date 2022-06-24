import copy
import json
import pickle
import gspread
import pandas
from .config import GOOGLE_CREDENTIAL_KEY_PATH
from typing import (
    List,
    Dict,
    Tuple,
)

_GOOGLE_CREDENTIAL_KEY_PATH = (
    # Key Path
    GOOGLE_CREDENTIAL_KEY_PATH
)
ANSWER_EMPTY_LEN = 0


def _exclude_empty_space(data: list):
    _data = data.copy()
    data_no_empty = []
    for d in _data:
        if d != "":
            data_no_empty.append(d)
    return data_no_empty


def _convert_info_to_list(key_list: list, value_list: list) -> List[dict]:
    data_list = []
    key_loc = 0
    for id_key in range(len(key_list)):
        # update the index of key
        if len(key_list[id_key]) > ANSWER_EMPTY_LEN:
            key_loc = id_key

        key = key_list[key_loc]
        for id_val, values in enumerate(value_list):
            val = values[id_key]
            if len(data_list) - 1 < id_val:
                data_list.append({key: [val]})
            else:
                if key in data_list[id_val].keys():
                    data_list[id_val][key].append(val)
                else:
                    data_list[id_val][key] = [val]
    return data_list


def _filter_empty(data_list: List[dict], key_list: list) -> List[dict]:
    _data_list = copy.deepcopy(data_list)
    key_loc = 0
    for id_key in range(len(key_list)):
        if len(key_list[id_key]) > ANSWER_EMPTY_LEN:
            key_loc = id_key
            if key_loc > 0:
                key = key_list[key_loc]
                for id_data_list in range(len(_data_list)):
                    if "" in _data_list[id_data_list][key]:
                        data_no_empty = _exclude_empty_space(
                            _data_list[id_data_list][key]
                        )
                        if len(data_no_empty) == 0:
                            _data_list[id_data_list][key] = ["No Answer"]
                        else:
                            _data_list[id_data_list][key] = data_no_empty
    return _data_list


def _encode_list2dict(data_list: List[list]):
    question_list = data_list[0].copy()  # Main question
    # category_list = data_list[1].copy()  # Sub category
    customer_responase_list = data_list[2:].copy()  # Customer response

    # convert information to the list of dict
    data_result = _convert_info_to_list(
        key_list=question_list, value_list=customer_responase_list
    )

    # remove empty values in dictionry
    data_result = _filter_empty(data_list=data_result, key_list=question_list)

    del data_list, question_list, customer_responase_list

    return data_result


def export_google_sheet(filename: str, sheetname: str):
    # open google sheet
    gc = gspread.service_account(filename=GOOGLE_CREDENTIAL_KEY_PATH)
    file = gc.open(filename)
    sheet = file.worksheet(sheetname)
    try:
        return sheet.get_all_records()  # dict
    # if calling dict, gspread.exceptions.GSpreadException: the given 'expected_headers' are not uniques
    except gspread.exceptions.GSpreadException:
        # TODO: add key, value index in variable
        return _encode_list2dict(data_list=sheet.get_all_values())


def save_data(filename: str, data):
    type = filename.split(".")[-1]
    if type == "pickle":
        with open(filename, "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    elif type == "json":
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        raise Exception("type must be pickle or json")


def load_data(filename: str):
    if filename.split(".")[-1] == "pickle":
        with open(filename, "rb") as f:
            data = pickle.load(f)
    elif filename.split(".")[-1] == "json":
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        raise Exception("type must be pickle or json")

    return data


def convert_pickle2json(file: str):
    if file[-6:] != "pickle":
        raise Exception("file must be a pickle file")

    # open pickle file
    with open(file, "rb") as f:
        obj = pickle.load(f)

    # convert pickle object to json object
    json_obj = json.loads(json.dumps(obj, default=str))

    file_json = file.split(".")
    file_json = "." + file_json[1] + ".json"

    # write the json file
    with open(file_json, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)

    del json_obj, file_json


def pairup_str_int(
    data_list: List[Dict[str, str]],
    key_dict: Dict[str, int],
    value_dict: Dict[str, int],
) -> List[Dict[int, int]]:
    _data_list = []
    for data in data_list:
        data_int = {}
        for key_str, val_str in data.items():
            key_int = key_dict[key_str]  # question id
            if isinstance(val_str, list):
                val_int = [value_dict[key_int][ans] for ans in val_str]
            else:
                val_int = value_dict[key_int][str(val_str)]
            data_int[key_int] = val_int
        _data_list.append(data_int)
    return _data_list


def extract_index_key_value(data_list: List[Dict[str, str]]) -> Tuple[dict, dict]:
    key_list = list(data_list[0].keys())
    key_dict = {str(key): id_key for id_key, key in enumerate(key_list)}

    value_list = []
    for data in data_list:
        for id_key, value in enumerate(data.values()):
            if len(value_list) - 1 < id_key:
                if isinstance(value, list):
                    value_list.append(copy.deepcopy(value))
                else:
                    value_list.append([copy.deepcopy(value)])
            else:
                if isinstance(value, list):
                    for val in value:
                        if val not in value_list[id_key]:
                            value_list[id_key].append(val)
                else:
                    if value not in value_list[id_key]:
                        value_list[id_key].append(value)

    value_dict = {}
    for qid, value in enumerate(value_list):
        value_dict[qid] = {str(val): id_val for id_val, val in enumerate(value)}

        for val in value:
            if "," in val:
                print(val)

    return key_dict, value_dict
