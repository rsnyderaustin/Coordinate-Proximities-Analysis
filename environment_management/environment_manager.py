import logging

import stack
from .map_classes import FileToUnitManagersMap, FileToRtreeAnalyzerMap, FileToDataFrameMap
from rtree_modules import rtree_analysis
from units import OutpostsManager, ScoutsManager
from . import unit_names_combinations_manager
from io_handling import dataframe_loading as df_load, unit_file, output_handling

logging.basicConfig(level=logging.INFO)


class EnvironmentManager:

    def __init__(self,
                 outpost_unit_files: set[unit_file.UnitFile],
                 scout_unit_files: set[unit_file.UnitFile]
                 ):

        self.outpost_unit_files = outpost_unit_files
        self.scout_unit_files = scout_unit_files

        self.file_to_rtree_analyzer_map = None
        self.unit_names_combinations_manager = None

        self.func_stack = stack.FunctionStack()
        self.done_called = False

    def _create_file_to_dataframe_map(self) -> FileToDataFrameMap:
        """
        Reads file information from UnitFile objects into a DataFrame, and then loads that into a
        FileToDataFrameMap class object.

        :return: FileToDataFrameMap object loaded with DataFrames from Outpost and Scout UnitFile objects
        """

        file_to_df_map = FileToDataFrameMap()
        for outpost_file in self.outpost_unit_files:
            column_names = outpost_file.get_all_column_names()
            df = df_load.load_dataframe(file_path=outpost_file.file_path,
                                        column_names=column_names,
                                        sheet_name=outpost_file.sheet_name)
            logging.info(f"DataFrame at file path '{outpost_file.file_path}' loaded.")
            file_to_df_map.add_dataframe(name=outpost_file.file_alias,
                                         unit_type='outpost',
                                         dataframe=df)
        for scout_file in self.scout_unit_files:
            column_names = scout_file.get_all_column_names()
            df = df_load.load_dataframe(file_path=scout_file.file_path,
                                        column_names=column_names,
                                        sheet_name=scout_file.sheet_name)
            logging.info(f"DataFrame at file path '{scout_file.file_path}' loaded.")
            file_to_df_map.add_dataframe(name=scout_file.file_alias,
                                         unit_type='scout',
                                         dataframe=df)
        return file_to_df_map

    def _create_rtree_analyzer_map(self, file_to_unit_managers_map: FileToUnitManagersMap) -> FileToRtreeAnalyzerMap:
        """
        Uses the ScoutManager's from the FileToUnitManagersMap to generate RtreeAnalyzer class objects,
        and then load them into the FileToRtreeAnalyzerMap class object.

        :param file_to_unit_managers_map: FileToUnitManagersMap object loaded with UnitManagers
        :return: FileToRtreeAnalyzerMap loaded with RtreeAnalyzer class objects
        """
        rtree_map = FileToRtreeAnalyzerMap()
        for scout_file in self.scout_unit_files:
            scout_manager = file_to_unit_managers_map.get_manager(name=scout_file.file_alias,
                                                                  unit_type='scout')
            scout_coordinates = scout_manager.get_all_scout_coordinates()
            new_rtree_analyzer = rtree_analysis.RtreeAnalyzer()
            new_rtree_analyzer.insert_coordinates_into_rtree(coordinates=scout_coordinates)

            rtree_map.add_rtree_analyzer(name=scout_file.file_alias,
                                         rtree_analyzer=new_rtree_analyzer)
        return rtree_map

    def _create_unit_managers_map(self, file_to_df_map: FileToDataFrameMap) -> FileToUnitManagersMap:
        """

        :param file_to_df_map: FileToDataFrameMap class object loaded with DataFrames for each UnitFile
            object in the EnvironmentManager
        :return: FileToUnitManagersMap class object loaded with UnitManager class objects for each Outpost and Scout
            UnitFile class object in the EnvironmentManager
        """
        file_to_unit_managers_map = FileToUnitManagersMap()
        for outpost_file in self.outpost_unit_files:
            dataframe = file_to_df_map.get_dataframe(name=outpost_file.file_alias,
                                                     unit_type='outpost')

            outpost_manager = OutpostsManager(name=outpost_file.file_alias)
            outpost_manager.create_outposts(dataframe=dataframe,
                                            lat_column_name=outpost_file.latitude_column_name,
                                            lon_column_name=outpost_file.longitude_column_name,
                                            extra_column_names=outpost_file.extra_column_names)
            file_to_unit_managers_map.add_manager(manager=outpost_manager,
                                                  name=outpost_file.file_alias,
                                                  unit_type='outpost')

        for scout_file in self.scout_unit_files:
            dataframe = file_to_df_map.get_dataframe(name=scout_file.file_alias,
                                                     unit_type='scout')

            scout_manager = ScoutsManager(name=scout_file.file_alias)
            scout_manager.create_scouts(dataframe=dataframe,
                                        lat_column_name=scout_file.latitude_column_name,
                                        lon_column_name=scout_file.longitude_column_name,
                                        extra_column_names=scout_file.extra_column_names)
            file_to_unit_managers_map.add_manager(manager=scout_manager,
                                                  name=scout_file.file_alias,
                                                  unit_type='scout')
        return file_to_unit_managers_map

    def _fill_unit_names_combinations_manager(self, file_to_unit_managers_map):
        """
        Loads the UnitNamesCombinationsManager class object with the copies of its proper UnitManager objects.

        :param file_to_unit_managers_map: FileToUnitManagersMap object loaded with UnitManagers
        """
        file_processing_combinations = self.unit_names_combinations_manager.combinations

        # Fill each NameCombinations object with its appropriate, un-queried unit managers
        for name_combination in file_processing_combinations:
            outpost_name = name_combination.outpost_name
            outpost_manager = file_to_unit_managers_map.get_manager(name=outpost_name,
                                                                    unit_type='outpost',
                                                                    should_copy=True)
            name_combination.add_outpost_manager(outpost_manager)

            scouts_managers = set()
            for scout_name in name_combination.scout_names:
                scout_manager = file_to_unit_managers_map.get_manager(name=scout_name,
                                                                      unit_type='scout',
                                                                      should_copy=True)
                scouts_managers.add(scout_manager)
            name_combination.add_scouts_managers(scouts_managers)

    def _process_environment(self, scout_extra_column_names: list[str]):
        """

        :param scout_extra_column_names: The extra column names apart from latitude and longitude column names
        for variables analysis requested in the analysis functions.
        """
        for unit_file_obj in self.scout_unit_files:
            if unit_file_obj.extra_column_names:
                unit_file_obj.extra_column_names.extend(scout_extra_column_names)
            else:
                unit_file_obj.extra_column_names = scout_extra_column_names

        file_to_df_map = self._create_file_to_dataframe_map()

        # SubstringToUnitManagersMap stores only the base-loaded outposts to be copied from later.
        file_to_unit_managers_map = self._create_unit_managers_map(file_to_df_map)

        self.unit_names_combinations_manager = unit_names_combinations_manager.UnitNamesCombinationsManager(
            outpost_files=self.outpost_unit_files,
            scout_files=self.scout_unit_files
        )

        self._fill_unit_names_combinations_manager(file_to_unit_managers_map)

        self.file_to_rtree_analyzer_map = self._create_rtree_analyzer_map(file_to_unit_managers_map)

    def process_analysis_functions(self):
        """
        This is the function to call after all analysis functions have been called on the EnvironmentManager class
        object. This function is only intended to be called one time. Any subsequent analysis function calls after
        calling process_analysis_functions will immediately call that analysis function on the EnvironmentManager,
        instead of adding it to the stack, and will not consider a higher scan range. This could be fixed in the future,
        however there isn't a clear use for calling process_analysis_functions multiple times at the moment.
        """
        self.done_called = True

        # Find the maximum scan range requested in the analysis functions, and the extra variable column
        # names that should be read from the DataFrames
        max_scan_range = 0
        scout_extra_column_names = []
        for func, kwargs in self.func_stack.function_generator():
            if 'scan_range' in kwargs and kwargs['scan_range'] > max_scan_range:
                max_scan_range = kwargs['scan_range']
            if 'variable' in kwargs and kwargs['variable'] not in scout_extra_column_names:
                scout_extra_column_names.append(kwargs['variable'])

        self._process_environment(scout_extra_column_names=scout_extra_column_names)

        for names_combination in self.unit_names_combinations_manager.combinations:
            outposts_manager = names_combination.outposts_manager
            scouts_managers = names_combination.scouts_managers

            for scouts_manager in scouts_managers:
                scouts_manager_name = scouts_manager.name
                rtree_analyzer = self.file_to_rtree_analyzer_map.get_rtree_analyzer(name=scouts_manager_name)
                self._load_scouts_into_outposts_manager(scan_range=max_scan_range,
                                                        outposts_manager=outposts_manager,
                                                        scouts_manager=scouts_manager,
                                                        rtree_analyzer=rtree_analyzer)

        for func, kwargs in self.func_stack.function_generator():
            func(**kwargs)

    @staticmethod
    def _load_scouts_into_outposts_manager(scan_range, outposts_manager, scouts_manager, rtree_analyzer):
        for outpost_coordinate, outpost in outposts_manager.outpost_generator():
            distances_to_coordinates_obj = rtree_analyzer.find_coordinates_around_point(
                reference_coordinate=outpost_coordinate,
                scan_range=scan_range
            )
            for scout_coordinate, distance in distances_to_coordinates_obj.coordinate_and_distance_generator():
                scouts_at_coordinate = scouts_manager.get_scouts(coordinate=scout_coordinate)
                outpost.add_scouts(scouts=scouts_at_coordinate,
                                   distance=distance)
        logging.info(f"Scouts from ScoutsManager {scouts_manager.name} loaded into OutpostsManager "
                     f"{outposts_manager.name}")

    def scout_in_range_tf(self, scan_range):
        """
        For each Outpost, determines whether there is a Scout within the specified scan range.
        :param scan_range: Requested range from each outpost to consider Scout objects.
        """
        if self.done_called:
            name_combinations = self.unit_names_combinations_manager.combinations
            for combination in name_combinations:
                combination.outposts_manager.scout_in_range_tf(scan_range=scan_range)
                logging.info(f"scout_in_range_tf processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.func_stack.add_to_stack(self.scout_in_range_tf,
                                         scan_range=scan_range)

    def num_scouts_in_range(self, scan_range):
        """
        For each Outpost, determines the number of Scouts within the specified scan range.
        :param scan_range: Requested range from each outpost to consider Scout objects.
        """
        if self.done_called:
            name_combinations = self.unit_names_combinations_manager.combinations
            for combination in name_combinations:
                combination.outposts_manager.num_scouts_in_range(scan_range=scan_range)
                logging.info(f"num_scouts_in_range processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.func_stack.add_to_stack(self.num_scouts_in_range,
                                         scan_range=scan_range)

    def num_scouts_in_range_by_variable(self, scan_range, variable, target_value):
        """
        For each Outpost, determines the number of Scouts within the specified scan range that have the target value for
        the specified variable.

        :param scan_range: Requested range from each outpost to consider Scout objects.
        :param variable: The column name determining whether a Scout should be considered or not.
        :param target_value: The target value determining whether a Scout should be considered or not.
        """
        if self.done_called:
            name_combinations = self.unit_names_combinations_manager.combinations
            for combination in name_combinations:
                combination.outposts_manager.num_scouts_in_range_by_variable(scan_range=scan_range,
                                                                             variable=variable,
                                                                             target_value=target_value)
                logging.info(f"count_scouts_by_variable processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.func_stack.add_to_stack(self.num_scouts_in_range_by_variable,
                                         scan_range=scan_range,
                                         variable=variable,
                                         target_value=target_value)

    def average_scouts_by_variable(self, scan_range, variable):
        """
        For each Outpost, determines the average numeric value for the specified variable for Scouts within
        the specified range.
        :param scan_range: Requested range from each outpost to consider Scout objects.
        :param variable: The column name determining whether a Scout should be considered or not.
        """
        if self.done_called:
            name_combinations = self.unit_names_combinations_manager.combinations
            for combination in name_combinations:
                combination.outposts_manager.average_scouts_by_variable(scan_range=scan_range,
                                                                        variable=variable)
                logging.info(
                    f"average_scouts_by_variable processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.func_stack.add_to_stack(self.average_scouts_by_variable,
                                         scan_range=scan_range,
                                         variable=variable)

    def nearest_scout(self, scan_range):
        """
        For each Outpost, determines the nearest Scout within the specified range.
        :param scan_range: Requested range from each outpost to consider Scout objects.
        """
        if self.done_called:
            name_combinations = self.unit_names_combinations_manager.combinations
            for combination in name_combinations:
                combination.outposts_manager.nearest_scout(scan_range)
                logging.info(
                    f"nearest_scout processed for OutpostsManager {combination.outposts_manager.name}.")
        else:
            self.func_stack.add_to_stack(self.nearest_scout,
                                         scan_range=scan_range)

    def _compile_query_data_into_dict(self) -> dict:
        """

        :return: Dict of DataFrames in the format "{ OutpostsManager.name: DataFrame }" for each UnitManagers name combination
            in the UnitNamesCombinationsManager.
        """
        dfs = {}
        for name_combination in self.unit_names_combinations_manager.combinations:
            combination_outposts_manager = name_combination.outposts_manager
            df = combination_outposts_manager.compile_query_data_into_df()
            dfs[combination_outposts_manager.name] = df
        return dfs

    def output_data_to_file(self, output_path):
        """
        Pulls the queried data results for each OutpostsUnitManager from the UnitNamesCombinationsManager, and outputs
        that data into the requested output file path.
        """
        dfs = self._compile_query_data_into_dict()
        output_handling.output_dfs_to_file(output_path=output_path,
                                           dataframes=dfs)
