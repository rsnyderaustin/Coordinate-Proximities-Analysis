from . import file_data_manager as fdm


class ProcessingCombination:

    def __init__(self, outposts_manager, scouts_managers):
        self.outposts_manager = outposts_manager
        self.scouts_managers = scouts_managers


class ProcessingCombinationsDataManager:

    def __init__(self):
        self.processing_combinations = set()

    def set_processing_combinations(self, file_data_manager: fdm.FileDataManager):
        outposts_managers = file_data_manager.get_all_outposts_managers(should_copy=True)
        for outposts_manager in outposts_managers:
            scouts_managers = file_data_manager.get_all_scouts_managers(should_copy=True)
            new_combination = ProcessingCombination(outposts_manager=outposts_manager,
                                                    scouts_managers=scouts_managers)
            self.processing_combinations.add(new_combination)
