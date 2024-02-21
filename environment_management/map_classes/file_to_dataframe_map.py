import logging
import pandas as pd


class FileToDataFrameMap:

    def __init__(self):
        self.outpost_map = {}
        self.scout_map = {}

        self.unit_type_map = {
            'outpost': self.outpost_map,
            'scout': self.scout_map
        }

    def _get_requested_unit_map(self, unit_type):
        if unit_type not in self.unit_type_map:
            raise KeyError(f"Requested unit type {unit_type} from FileSubstringToDataFrameMap.\n"
                           f"Valid unit types: {list(self.unit_type_map.keys())}")

        return self.unit_type_map[unit_type]

    def add_dataframe(self, unit_type: str, name: str, dataframe: pd.DataFrame):
        requested_map = self._get_requested_unit_map(unit_type)
        if name in requested_map:
            logging.info(
                f"Overwriting dataframe in FileSubstringToDataFrameMap for unit type {unit_type} with substring {name}.\n"
                f"Possibly an error.")

        requested_map[name] = dataframe

    def get_dataframe(self, unit_type: str, name: str):
        requested_map = self._get_requested_unit_map(unit_type)
        if name not in requested_map:
            raise KeyError(f"get_dataframe called for invalid substring key {name} with unit type {unit_type} on "
                           f"SubstringToDataFrameMap.")

        return requested_map[name]