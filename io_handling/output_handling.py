import logging
import os
import pandas as pd


def output_dfs_to_file(output_path, dataframes: dict):
    file_name = os.path.basename(output_path)
    base, extension = os.path.splitext(file_name)

    if extension in '.csv':
        for name, df in dataframes.items():
            index_col = [name for _ in range(len(df))]
            df.insert(loc=0, column='index', value=index_col)
        df_list = list(dataframes.values())
        df_concatted = pd.concat(df_list)

    output_success = False
    while not output_success:
        try:
            if extension in '.csv':
                df_concatted.to_csv(output_path, index=False)
                logging.info("Output DataFrame to .csv file at '{output_path}'")
            elif extension in '.xlsx':
                with pd.ExcelWriter(output_path) as writer:
                    for name, df in dataframes.items():
                        df.to_excel(writer, sheet_name=name, index=False)
                        logging.info(f"Output DataFrame to Excel sheet name '{name}'")
                logging.info(f"Output DataFrame to .xlsx at '{output_path}'")
            else:
                raise ValueError(f"Extension is not one of accepted values (.csv, .xlsx)\nExtension: '{extension}'")
        except PermissionError:
            print(f"Attempting to write to file {output_path}, but the file is currently open.\n"
                  f"Please close the file, then press any key to continue.")
            input()