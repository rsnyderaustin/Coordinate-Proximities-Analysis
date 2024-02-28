import logging


class ScoutDataMap:
    
    def __init__(self):
        self.data = {}

    def add_scout_data(self, variable_name, value):
        if variable_name in self.data:
            logging.info(
                f"Overwriting!\n\tscout_string '{variable_name}'\n\told data:{self.data[variable_name]}"
                f"\n\tnew data: {value}")

        self.data[variable_name] = value

    def get_scout_data(self, variable_name):
        if variable_name not in self.data:
            return None

        return self.data[variable_name]


class Scout:

    def __init__(self, coordinate: tuple):
        self.scout_data_map = ScoutDataMap()

        self.coordinate = coordinate

    def add_data(self, variable_name, value):
        self.scout_data_map.add_scout_data(variable_name=variable_name,
                                           value=value)

    def get_data(self, variable_name):
        return self.scout_data_map.get_scout_data(variable_name=variable_name)
