
class UnitFile:

    def __init__(self,
                 file_alias: str,
                 latitude_column_name: str,
                 longitude_column_name: str,
                 file_path: str,
                 extra_column_names: list[str] = None,
                 sheet_name: str = None
                 ):
        self.file_alias = file_alias
        self.latitude_column_name = latitude_column_name
        self.longitude_column_name = longitude_column_name
        self.file_path = file_path
        self.sheet_name = sheet_name

        self.extra_column_names = extra_column_names

    def get_all_column_names(self):
        if self.extra_column_names:
            combined_columns = self.extra_column_names + [self.latitude_column_name, self.longitude_column_name]
        else:
            combined_columns = [self.latitude_column_name, self.longitude_column_name]
        return combined_columns

    def add_extra_column_names(self, column_names):
        if self.extra_column_names:
            self.extra_column_names.extend(column_names)
        else:
            self.extra_column_names = column_names
