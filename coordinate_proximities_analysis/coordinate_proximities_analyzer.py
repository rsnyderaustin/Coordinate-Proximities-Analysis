import logging

from analysis_processing import analysis_processor
from environment_management import environment_manager
from io_handling import unit_file, output_handling
from stack import stack_analysis

logging.basicConfig(level=logging.INFO)


class CoordinateProximitiesAnalyzer:

    def __init__(self, outpost_unit_files: set[unit_file.UnitFile], scout_unit_files: set[unit_file.UnitFile]):
        self.environment_manager = environment_manager.EnvironmentManager(outpost_unit_files=outpost_unit_files,
                                                                          scout_unit_files=scout_unit_files)
        self.analysis_processor = analysis_processor.AnalysisProcessor(environment_manager=self.environment_manager)

    def process_analysis_functions(self, output_file_path: str):
        function_stack = self.analysis_processor.function_stack
        scan_range = max(stack_analysis.get_stack_values(function_stack=function_stack,
                                                         variable_name='scan_range'))
        scout_extra_column_names = set(stack_analysis.get_stack_values(function_stack=function_stack,
                                                                       variable_name='variable'))
        self.environment_manager.process_environment(scan_range=scan_range,
                                                     scout_extra_column_names=scout_extra_column_names)
        self.analysis_processor.process_functions()

        data_dict = self.environment_manager.compile_analysis_data_into_dict()
        output_handling.output_dfs_to_file(output_path=output_file_path,
                                           dataframes=data_dict)

    def scout_in_range_true_false(self, scan_range: int):
        self.analysis_processor.scout_in_range_t_f(scan_range=scan_range)

    def number_of_scouts_in_range(self, scan_range: int):
        self.analysis_processor.num_scouts_in_range(scan_range=scan_range)

    def number_of_scouts_in_range_by_variable(self, scan_range: int, variable_name: str, target_value):
        self.analysis_processor.num_scouts_in_range_by_variable(scan_range=scan_range,
                                                                variable=variable_name,
                                                                target_value=target_value)

    def average_of_variable_for_scouts_in_range(self, scan_range: int, variable_name: str):
        self.analysis_processor.avg_scouts_by_variable(scan_range=scan_range,
                                                       variable=variable_name)

    def nearest_scout(self, scan_range: int):
        self.analysis_processor.nearest_scout(scan_range=scan_range)
