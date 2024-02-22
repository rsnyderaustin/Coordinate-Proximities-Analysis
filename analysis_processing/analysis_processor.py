import logging

from .. import stack, environment_management as em


class AnalysisProcessor:

    def __init__(self, environment_manager: em.EnvironmentManager):
        self.environment_manager = environment_manager

        self.function_stack = stack.FunctionStack()
        self.done_called = False

    def process_functions(self):
        self.done_called = True
        for func, kwargs in self.function_stack.function_generator():
            func(**kwargs)

    def scout_in_range_t_f(self, scan_range: int):
        if self.done_called:
            processing_combinations = self.environment_manager.processing_combinations_data_manager
            for combination in processing_combinations:
                combination.outposts_manager.scout_in_range_tf(scan_range=scan_range)
                logging.info(f"scout_in_range_tf processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.function_stack.add_to_stack(self.scout_in_range_t_f,
                                             scan_range=scan_range)

    def num_scouts_in_range(self, scan_range: int):
        if self.done_called:
            processing_combinations = self.environment_manager.processing_combinations_data_manager
            for combination in processing_combinations:
                combination.outposts_manager.num_scouts_in_range(scan_range=scan_range)
                logging.info(f"num_scouts_in_range processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.function_stack.add_to_stack(self.num_scouts_in_range,
                                             scan_range=scan_range)

    def num_scouts_in_range_by_variable(self, scan_range: int, variable: str, target_value):
        if self.done_called:
            processing_combinations = self.environment_manager.processing_combinations_data_manager
            for combination in processing_combinations:
                combination.outposts_manager.num_scouts_in_range_by_variable(scan_range=scan_range,
                                                                             variable=variable,
                                                                             target_value=target_value)
                logging.info(
                    f"count_scouts_by_variable processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.function_stack.add_to_stack(self.num_scouts_in_range_by_variable,
                                             scan_range=scan_range,
                                             variable=variable,
                                             target_value=target_value)

    def avg_scouts_by_variable(self, scan_range: int, variable: str):
        if self.done_called:
            processing_combinations = self.environment_manager.processing_combinations_data_manager
            for combination in processing_combinations:
                combination.outposts_manager.average_scouts_by_variable(scan_range=scan_range,
                                                                        variable=variable)
                logging.info(
                    f"average_scouts_by_variable processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.function_stack.add_to_stack(self.avg_scouts_by_variable,
                                             scan_range=scan_range,
                                             variable=variable)

    def nearest_scout(self, scan_range: int):
        if self.done_called:
            processing_combinations = self.environment_manager.processing_combinations_data_manager
            for combination in processing_combinations:
                combination.outposts_manager.nearest_scout(scan_range)
                logging.info(
                    f"nearest_scout processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.function_stack.add_to_stack(self.nearest_scout,
                                             scan_range=scan_range)
