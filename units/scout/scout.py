import logging
from typing import Union


class ScoutDataMap:
    
    def __init__(self):
        self.scout_map = {}

    def add_scout_data(self, variable_name, value):
        if variable_name in self.scout_map:
            logging.info(
                f"Overwriting!\n\tscout_string '{variable_name}'\n\told data:{self.scout_map[variable_name]}"
                f"\n\tnew data: {value}")

        self.scout_map[variable_name] = value

    def get_scout_data(self, variable_name):
        if variable_name not in self.scout_map:
            return None

        return self.scout_map[variable_name]


class Scout:

    def __init__(self, coordinate: tuple):
        self.scout_data_map = ScoutDataMap()

        self.coordinate = coordinate

    def add_data(self, variable_name, value):
        self.scout_data_map.add_scout_data(variable_name=variable_name,
                                           value=value)

    def get_data(self, variable_name):
        return self.scout_data_map.get_scout_data(variable_name=variable_name)
