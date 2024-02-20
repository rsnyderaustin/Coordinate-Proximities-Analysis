import os

import pandas as pd


class FileSubstringMatchError(Exception):
    pass


class NoFileFoundForSubstringError(Exception):
    pass


def _get_file_extension(file_path):
    file_name = os.path.basename(file_path)
    base_name, extension = os.path.splitext(file_name)
    return extension


def load_dataframe(file_path: str, column_names: list, sheet_name=None) -> pd.DataFrame:
    """
    Base dataframe extraction function for processing Outposts.
    :param file_path: Internal file path for input. To be read into a Dataframe.
    :param column_names: Specifies the column names to be included in the resulting DataFrame.
    :param sheet_name: Excel-specific parameter denoting the sheet name in the input Excel file.
    :return: DataFrame from provided file path, filtered to the specified column names.
    """
    file_extension = _get_file_extension(file_path)
    if file_extension in ['.xls', '.xlsx']:
        if sheet_name:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
    elif file_extension in ['.csv']:
        df = pd.read_csv(file_path)
    else:
        raise Exception(f"File path {file_path} does not have one of valid extensions .csv, .xls, or .xlsx")
    if not set(column_names).issubset(set(df.columns)):
        raise ValueError(f"Column names not in the dataframe.\n\tRequested column names: {column_names}"
                         f"\n\tDataFrame column names: {df.columns}")

    return df[column_names]

