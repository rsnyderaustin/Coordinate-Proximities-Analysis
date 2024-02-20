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
        df_concatted.to_csv(output_path, index=False)
        logging.info("Output DataFrame to .csv file at '{output_path}'")
    elif extension in '.xlsx':
        with pd.ExcelWriter(output_path) as writer:
            for name, df in dataframes.items():
                df.to_excel(writer, sheet_name=name, index=False)
                logging.info(f"Output DataFrame to Excel sheet name '{name}'")
        logging.info(f"Output DataFrame to .xlsx at '{output_path}'")