import logging
from typing import Union


class OutpostDistancesToScoutsMap:

    def __init__(self):
        self.map = {}

    def add_scout_to_map(self, scout, distance):
        if distance in self.map:
            self.map[distance].append(scout)
        else:
            self.map[distance] = [scout]

    def get_scouts_at_distance(self, distance) -> Union[list, None]:
        if distance not in self.map:
            return None

        return self.map[distance]

    def get_sorted_distances_to_scouts(self):
        return sorted(self.map.items())
    

class OutpostDataMap:
    def __init__(self):
        self.outpost_map = {}

    def add_outpost_data(self, variable_name, value):
        if variable_name in self.outpost_map:
            logging.info(f"Overwriting!\n\toutpost_string '{variable_name}'\n\told data:{self.outpost_map[variable_name]}"
                         f"\n\tnew data: {value}")

        self.outpost_map[variable_name] = value

    def get_outpost_data(self, variable_name):
        if variable_name not in self.outpost_map:
            return None

        return self.outpost_map[variable_name]

    def get_data_names(self) -> list[str]:
        return list(self.outpost_map.keys())


class QueryDataMap:

    def __init__(self):
        self.query_map = {}

    def add_query_data(self, query_string, data):
        if query_string in self.query_map:
            logging.info(f"Overwriting!\n\tquery_string '{query_string}'\n\told data:{self.query_map[query_string]}"
                         f"\n\tnew data: {data}")

        self.query_map[query_string] = data

    def get_query_data(self, query_string):
        if query_string not in self.query_map:
            return None

        return self.query_map[query_string]

    def get_query_names(self) -> list[str]:
        return list(self.query_map.keys())


class Outpost:

    def __init__(self, coordinate: tuple):
        self.coordinate = coordinate

        self.query_data_map = QueryDataMap()
        self.outpost_data_map = OutpostDataMap()

        self.distances_to_scouts_map = OutpostDistancesToScoutsMap()

    def get_latitude(self):
        return self.coordinate[0]

    def get_longitude(self):
        return self.coordinate[1]

    def add_outpost_data(self, variable_name, value):
        self.outpost_data_map.add_outpost_data(variable_name=variable_name,
                                               value=value)

    def add_query_data(self, query_string, value):
        self.query_data_map.add_query_data(query_string=query_string,
                                           data=value)

    def get_all_query_data(self):
        if not self.query_data_map.query_map:
            return None

        return self.query_data_map.query_map

    def add_scouts(self, scouts, distance):
        for scout in scouts:
            self.distances_to_scouts_map.add_scout_to_map(scout=scout,
                                                          distance=distance)

    def get_sorted_distances_to_scouts(self) -> list:
        return self.distances_to_scouts_map.get_sorted_distances_to_scouts()

    def outpost_data_generator(self):
        for variable_name, value in self.outpost_data_map.outpost_map.items():
            yield variable_name, value

    def outpost_query_generator(self):
        for query_name, value in self.query_data_map.query_map.items():
            yield query_name, value

    def get_data_names(self):
        return self.outpost_data_map.get_data_names()

    def get_query_names(self):
        return self.query_data_map.get_query_names()

