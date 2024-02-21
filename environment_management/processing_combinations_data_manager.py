from io_handling import unit_file

class CombinationData:



class ProcessingCombinationsDataManager:

    def __init__(self):
        self.combinations = None

    def set_name_combinations(self, outpost_files: set[unit_file.UnitFile], scout_files: set[unit_file.UnitFile]):
        scout_names = {scout_file.file_alias for scout_file in scout_files}
        for outpost_file in outpost_files:
            outpost_name = outpost_file.file_alias
            new_combination = NameCombinations(outpost_name=outpost_name,
                                               scout_names=scout_names)
            file_combinations.add(new_combination)
        return file_combinations

