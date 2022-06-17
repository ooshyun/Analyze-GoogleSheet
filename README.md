Data Analyzing through Google Sheet
------------------------------------------------
*First of all, making the src/config.py to set the setup
- Example of src/config.py
    ```python
    GOOGLE_CREDENTIAL_KEY_PATH = # the path of the google credential file
    DATA_NAME = # names for making the final data
    FILE_NAME = # the names of google files  for making the final data
    SHEET_NAME = # the names of sheets, and it match the index with FILE_NAME
    RESULT_NAME = # the name of result
    ```

1. Tranlate Google Sheet to data storage(ex. pickle or json)
    1. Download Google Sheet data
        - Avoid empty cells
            1. empty category
            2. no answer
    2. Translate Google Sheet data to pickle/json data
        - Data Structure
    3. Save and Load data
    4. Pair up text to integer
        - Data Structure
            {
                "file_1": {
                    "question": question_dict_1,
                    "answer": answer_dict_1,
                    "data": data_paring_int_1,
                    "data_string": data_2,
                },
                "file_2_": {
                    "question": question_dict_2_,
                    "answer": answer_dict_2_,
                    "data": data_paring_int_2_,
                    "data_string": data_2,
                },
                ...
            }
        - Pair up data
            1. question     : question list text - int
            2. answer       : answer list   int(question) - answer - int
            3. data         : data          int(question) - int(answer)    
        - Raw data
            4. data_string  : raw data
    5. Save entire data

2. Anaylze(Continue...)