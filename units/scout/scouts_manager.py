import pandas as pd

from units.scout import scout


class CoordinateScoutsMap:

    def __init__(self):
        self.scouts = {}

    def add_scout(self, scout_object):
        coordinate = scout_object.coordinate
        if coordinate in self.scouts:
            self.scouts[coordinate].append(scout_object)
        else:
            self.scouts[coordinate] = [scout_object]

    def get_scouts(self, coordinate):
        if coordinate not in self.scouts:
            raise KeyError(f"Requested nonextistent coordinate {coordinate} from CoordinateScoutsMap.")

        return self.scouts[coordinate]

    def get_map(self):
        return self.scouts


class ScoutsManager:

    def __init__(self, name: str):
        self.name = name
        self._coordinate_scouts_map = CoordinateScoutsMap()

    @staticmethod
    def _get_coordinate(df, row_index, latitude_column_name, longitude_column_name):
        latitude = df.loc[row_index, latitude_column_name]
        longitude = df.loc[row_index, longitude_column_name]
        coordinate = (latitude, longitude)
        return coordinate

    def create_scouts(self, dataframe: pd.DataFrame, lat_column_name: str, lon_column_name: str,
                      extra_column_names: set):
        coordinates = []
        for row_index in dataframe.index:
            coordinate = self._get_coordinate(dataframe, row_index, lat_column_name, lon_column_name)
            coordinates.append(coordinate)
            new_scout = scout.Scout(coordinate=coordinate)

            if not extra_column_names:
                continue

            for i, col_name in enumerate(extra_column_names):
                value = dataframe.loc[row_index, col_name]
                new_scout.add_data(variable_name=col_name, value=value)

            self._coordinate_scouts_map.add_scout(new_scout)

    def get_scouts(self, coordinate: tuple):
        return self._coordinate_scouts_map.get_scouts(coordinate=coordinate)

    def scout_generator(self):
        scouts_map = self._coordinate_scouts_map.get_map()

        for coordinate, scouts_list in scouts_map.items():
            for scout in scouts_list:
                yield coordinate, scout

    def get_all_scout_coordinates(self) -> list[tuple]:
        """

        :return: All scout coordinates in a list of tuples.
        """
        scout_coordinates = list(self._coordinate_scouts_map.scouts.keys())
        return scout_coordinates
