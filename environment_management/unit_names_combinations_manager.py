from io_handling import unit_file


class NameCombinations:

    def __init__(self, outpost_name: str, scout_names: set[str]):
        self.outpost_name = outpost_name
        self.scout_names = scout_names
        self.outposts_manager = None
        self.scouts_managers = None

    def add_outpost_manager(self, outposts_manager):
        self.outposts_manager = outposts_manager

    def add_scouts_managers(self, scouts_managers):
        self.scouts_managers = scouts_managers
        

class UnitNamesCombinationsManager:

    def __init__(self, outpost_files: set[unit_file.UnitFile], scout_files: set[unit_file.UnitFile]):
        self.combinations = self._combine_names(outpost_files, scout_files)

    @staticmethod
    def _combine_names(outpost_files: set[unit_file.UnitFile], scout_files: set[unit_file.UnitFile]) -> set[NameCombinations]:
        file_combinations = set()
        scout_names = {scout_file.file_alias for scout_file in scout_files}
        for outpost_file in outpost_files:
            outpost_name = outpost_file.file_alias
            new_combination = NameCombinations(outpost_name=outpost_name,
                                               scout_names=scout_names)
            file_combinations.add(new_combination)
        return file_combinations

