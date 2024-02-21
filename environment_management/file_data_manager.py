import logging


class FileData:

    def __init__(self, file_name: str, unit_type: str):
        self.file_name = file_name
        self.unit_type = unit_type

        self.dataframe = None
        self.unit_manager = None
        self.rtree = None


class FileDataManager:

    def __init__(self):
        self.files = {}
    
    def add_file_data_object(self, file_name: str, unit_type: str):
        if (file_name, unit_type) in self.files:
            logging.debug(f"Overwriting FileData in FileDataManager with file_name '{file_name}' and "
                          f"unit_type '{unit_type}'")
        
        self.files[(file_name, unit_type)] = FileData(file_name=file_name, unit_type=unit_type)

    def add_data(self, file_name, unit_type, dataframe = None, unit_manager = None, rtree = None):
        file_data = self.files[(file_name, unit_type)]
        if dataframe is not None:
            file_data.dataframe = dataframe

        if unit_manager is not None:
            file_data.unit_manager = unit_manager

        if rtree is not None:
            file_data.rtree = rtree
    
    def get_dataframe(self, file_name, unit_type):
        file_data_obj = self.files[(file_name, unit_type)]
        return file_data_obj.dataframe
    
    def get_unit_manager(self, file_name, unit_type):
        file_data_obj = self.files[(file_name, unit_type)]
        return file_data_obj.unit_manager
    
    def get_rtree(self, file_name, unit_type):
        file_data_obj = self.files[(file_name, unit_type)]
        return file_data_obj.rtree

