from src import (
    export_google_sheet,
    save_data,
    load_data,
    pairup_str_int,
    extract_index_key_value,
    # convert_pickle2json,
)
from src import DATA_NAME, FILE_NAME, SHEET_NAME, RESULT_NAME

if __name__ == "__main__":
    print("This is a project for analyzing google sheet")
    print("-" * 50)

    result_name = RESULT_NAME
    data_type = ".json"  # or ".pickle"
    file_path_data = "./data/data_" + result_name + data_type

    def convert_google_sheet_to_json(result_path):
        """
        For string contents of google sheet, convert to json and make index dictionary for string
        """
        # file name, previouw it should have permission in credential and in google sheet
        data_name_list = DATA_NAME
        file_name_list = FILE_NAME
        sheetname = SHEET_NAME

        data_result = {}
        for index_data, file_name in enumerate(file_name_list):
            data_name = data_name_list[index_data]
            file_path = "./data/data_" + data_name + data_type

            # load from google sheet and save
            data = export_google_sheet(file_name, sheetname)
            save_data(file_path, data)

            # load data files
            data = load_data(file_path)

            # extract question and answer list
            question_dict, answer_dict = extract_index_key_value(data)

            # match string to number in question and answer
            data_paring_int = pairup_str_int(
                data_list=data, key_dict=question_dict, value_dict=answer_dict
            )

            # exchange key(str) and value(int)
            question_dict = {value: key for key, value in question_dict.items()}
            for id_question, _answer_dict in answer_dict.items():
                answer_dict[id_question] = {
                    value: key for key, value in _answer_dict.items()
                }

            data_result[data_name] = {
                "question": question_dict,
                "answer": answer_dict,
                "data": data_paring_int,
                "data_string": data,
            }

        save_data(result_path, data_result)

    convert_google_sheet_to_json(file_path_data)
