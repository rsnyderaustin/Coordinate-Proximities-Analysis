import copy
import logging


class FileToUnitManagersMap:

    def __init__(self):
        self.outposts_managers_map = {}
        self.scouts_managers_map = {}

        self.unit_type_map = {
            'outpost': self.outposts_managers_map,
            'scout': self.scouts_managers_map
        }

    def _get_requested_unit_map(self, unit_type):
        if unit_type in self.unit_type_map:
            return self.unit_type_map[unit_type]
        else:
            raise KeyError(f"Requested unit type {unit_type} from FileSubstringToDataFrameMap.\n"
                           f"Valid unit types: {list(self.unit_type_map.keys())}")

    def add_manager(self, name, manager, unit_type):
        manager_map = self._get_requested_unit_map(unit_type=unit_type)

        if name in manager_map:
            logging.info(
                f"Overwriting manager in FileSubstringToUnitManagersMap for unit type {unit_type} with substring {name}.\n"
                f"Possibly an error.")

        manager_map[name] = manager

    def get_manager(self, name, unit_type, should_copy=False):
        manager_map = self._get_requested_unit_map(unit_type=unit_type)

        if name not in manager_map:
            raise KeyError(f"get_manager called for unit type {unit_type} for nonexistent substring {name} from \n"
                           f"FileSubstringToUnitManagersMap.")

        if should_copy:
            return copy.deepcopy(manager_map[name])
        else:
            return manager_map[name]
