from typing import Union

import pandas as pd

from units.outpost.outpost import Outpost
from . import outposts_analysis_functions


class CoordinateToOutpostsMap:

    def __init__(self):
        self.outposts = {}

    def add_outpost(self, outpost):
        coordinate = outpost._coordinate
        if coordinate in self.outposts:
            self.outposts[coordinate].append(outpost)
        else:
            self.outposts[coordinate] = [outpost]

    def get_outposts(self, coordinate) -> Union[list[Outpost], None]:
        if coordinate not in self.outposts:
            return None

        return self.outposts[coordinate]

    def get_map(self):
        return self.outposts


class OutpostsManager:

    def __init__(self, name: str):
        self.name = name
        # coordinate: Outpost
        self.coordinate_to_outposts_map = CoordinateToOutpostsMap()

    def create_outposts(self, dataframe: pd.DataFrame, lat_column_name: str, lon_column_name: str,
                        extra_column_names: Union[list, None] = None):
        for row_index in dataframe.index:
            latitude = dataframe.loc[row_index, lat_column_name]
            longitude = dataframe.loc[row_index, lon_column_name]
            coordinate = (latitude, longitude)

            new_outpost = Outpost(coordinate=coordinate)

            if extra_column_names:
                for extra_column_name in extra_column_names:
                    new_outpost.add_outpost_data(variable_name=extra_column_name,
                                                 value=dataframe.loc[row_index, extra_column_name])

            self.coordinate_to_outposts_map.add_outpost(outpost=new_outpost)

    def outpost_generator(self) -> tuple[tuple, Outpost]:
        outpost_map = self.coordinate_to_outposts_map.get_map()

        for coordinate, outpost_list in outpost_map.items():
            for outpost in outpost_list:
                yield coordinate, outpost

    def scout_in_range_tf(self, scan_range):
        for coordinate, outpost in self.outpost_generator():
            file_substring_result = outposts_analysis_functions.scout_in_range_tf(outpost=outpost,
                                                                                  scan_range=scan_range
                                                                                  )
            query_str = f"Scout found within {scan_range} miles"
            outpost.add_query_data(query_string=query_str,
                                   value=file_substring_result
                                   )

    def num_scouts_in_range(self, scan_range):
        for coordinate, outpost in self.outpost_generator():
            file_substring_result = outposts_analysis_functions.num_scouts_in_range(outpost=outpost,
                                                                                    scan_range=scan_range
                                                                                    )
            query_str = f"Number of scouts within {scan_range} miles"
            outpost.add_query_data(query_string=query_str,
                                   value=file_substring_result
                                   )

    def num_scouts_in_range_by_variable(self, scan_range, variable, target_value):
        for coordinate, outpost in self.outpost_generator():
            file_substring_result = outposts_analysis_functions.count_scouts_by_variable(outpost=outpost,
                                                                                         scan_range=scan_range,
                                                                                         variable=variable,
                                                                                         target_value=target_value
                                                                                         )
            query_str = (
                f"Number of scouts within {scan_range} miles with variable '{variable}' equal to target value "
                f"'{target_value}'")
            outpost.add_query_data(query_string=query_str,
                                   value=file_substring_result)

    def average_scouts_by_variable(self, scan_range, variable):
        for coordinate, outpost in self.outpost_generator():
            file_substring_result = outposts_analysis_functions.average_scouts_by_variable(outpost=outpost,
                                                                                           scan_range=scan_range,
                                                                                           variable=variable
                                                                                           )
            query_str = f"Average '{variable}' of scouts within {scan_range} miles"
            outpost.add_query_data(query_string=query_str,
                                   value=file_substring_result
                                   )

    def nearest_scout(self, scan_range):
        for coordinate, outpost in self.outpost_generator():
            result = outposts_analysis_functions.nearest_scout(outpost=outpost)
            query_str = f"Nearest scout within {scan_range} miles."
            outpost.add_query_data(query_string=query_str,
                                   value=result
                                   )

    def compile_query_data_into_df(self):

        # Initialize blank key values in dict
        output_data = {
            'latitude': [],
            'longitude': []
        }
        gen = self.outpost_generator()
        first_outpost = next(gen)[1]
        outpost_variable_names = first_outpost.get_data_names()
        for variable_name in outpost_variable_names:
            output_data[variable_name] = []
        outpost_query_names = first_outpost.get_query_names()
        for query_name in outpost_query_names:
            output_data[query_name] = []

        gen = self.outpost_generator()
        for coordinate, outpost in gen:
            output_data['latitude'].append(outpost.get_latitude())
            output_data['longitude'].append(outpost.get_longitude())
            for key, value in outpost.outpost_data_generator():
                output_data[key].append(value)
            for key, value in outpost.outpost_query_generator():
                output_data[key].append(value)

        df = pd.DataFrame(output_data)
        return df
