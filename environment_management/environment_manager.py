import logging

import stack
from rtree_modules import rtree_analysis
from units import OutpostsManager, ScoutsManager
from . import processing_combinations_data_manager as pcdm, file_data_manager
from io_handling import dataframe_loading as df_load, unit_file


class EnvironmentManager:

    def __init__(self,
                 outpost_unit_files: set[unit_file.UnitFile],
                 scout_unit_files: set[unit_file.UnitFile]
                 ):

        self.outpost_unit_files = outpost_unit_files
        self.scout_unit_files = scout_unit_files

        self.file_data_manager = file_data_manager.FileDataManager()
        self.processing_combinations_data_manager = pcdm.ProcessingCombinationsDataManager()

        self.func_stack = stack.FunctionStack()

    def _populate_file_data_manager(self):
        for outpost_unit_file in self.outpost_unit_files:
            name = outpost_unit_file.file_alias
            self.file_data_manager.add_file_data_object(file_name=name,
                                                        unit_type='outpost')
        for scout_unit_file in self.scout_unit_files:
            name = scout_unit_file.file_alias
            self.file_data_manager.add_file_data_object(file_name=name,
                                                        unit_type='scout')

    def _add_dataframes_to_file_data_manager(self):
        for outpost_file in self.outpost_unit_files:
            column_names = outpost_file.get_all_column_names()
            df = df_load.load_dataframe(file_path=outpost_file.file_path,
                                        column_names=column_names,
                                        sheet_name=outpost_file.sheet_name)
            logging.info(f"DataFrame at file path '{outpost_file.file_path}' loaded.")
            self.file_data_manager.add_data(file_name=outpost_file.file_alias,
                                            unit_type='outpost',
                                            dataframe=df)
        for scout_file in self.scout_unit_files:
            column_names = scout_file.get_all_column_names()
            df = df_load.load_dataframe(file_path=scout_file.file_path,
                                        column_names=column_names,
                                        sheet_name=scout_file.sheet_name)
            logging.info(f"DataFrame at file path '{scout_file.file_path}' loaded.")
            self.file_data_manager.add_data(file_name=scout_file.file_alias,
                                            unit_type='scout',
                                            dataframe=df)

    def _add_unit_managers_to_file_data_manager(self):
        for outpost_file in self.outpost_unit_files:
            dataframe = self.file_data_manager.get_dataframe(file_name=outpost_file.file_alias,
                                                             unit_type='outpost')

            outpost_manager = OutpostsManager(name=outpost_file.file_alias)
            outpost_manager.create_outposts(dataframe=dataframe,
                                            lat_column_name=outpost_file.latitude_column_name,
                                            lon_column_name=outpost_file.longitude_column_name,
                                            extra_column_names=outpost_file.extra_column_names)
            self.file_data_manager.add_data(file_name=outpost_file.file_alias,
                                            unit_type='outpost',
                                            unit_manager=outpost_manager)

        for scout_file in self.scout_unit_files:
            dataframe = self.file_data_manager.get_dataframe(file_name=scout_file.file_alias,
                                                             unit_type='scout')

            scout_manager = ScoutsManager(name=scout_file.file_alias)
            scout_manager.create_scouts(dataframe=dataframe,
                                        lat_column_name=scout_file.latitude_column_name,
                                        lon_column_name=scout_file.longitude_column_name,
                                        extra_column_names=scout_file.extra_column_names)
            self.file_data_manager.add_data(file_name=scout_file.file_alias,
                                            unit_type='scout',
                                            unit_manager=scout_manager)

    def _add_rtrees_to_file_data_manager(self):
        for scout_file in self.scout_unit_files:
            scouts_manager = self.file_data_manager.get_unit_manager(file_name=scout_file.file_alias,
                                                                     unit_type='scout')
            scout_coordinates = scouts_manager.get_all_scout_coordinates()
            new_rtree_analyzer = rtree_analysis.RtreeAnalyzer()
            new_rtree_analyzer.insert_coordinates_into_rtree(coordinates=scout_coordinates)

            self.file_data_manager.add_data(file_name=scout_file.file_alias,
                                            unit_type='scout',
                                            rtree=new_rtree_analyzer)

    def process_environment(self, scan_range: int, scout_extra_column_names: set[str]):
        for unit_file_obj in self.scout_unit_files:
            unit_file_obj.add_extra_column_names(column_names=scout_extra_column_names)

        self._populate_file_data_manager()

        self._add_dataframes_to_file_data_manager()

        self._add_unit_managers_to_file_data_manager()

        self._add_rtrees_to_file_data_manager()

        self.processing_combinations_data_manager.set_processing_combinations(file_data_manager=self.file_data_manager)

        for processing_combination in self.processing_combinations_data_manager.processing_combinations:
            outposts_manager = processing_combination.outposts_manager
            scouts_managers = processing_combination.scouts_managers

            for scouts_manager in scouts_managers:
                rtree_analyzer = self.file_data_manager.get_rtree(file_name=scouts_manager.name)
                self._load_scouts_into_outposts_manager(scan_range=scan_range,
                                                        outposts_manager=outposts_manager,
                                                        scouts_manager=scouts_manager,
                                                        rtree_analyzer=rtree_analyzer)

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

    def compile_analysis_data_into_dict(self) -> dict:
        """

        :return: Dict of DataFrames in the format "{ OutpostsManager.name: DataFrame }" for each UnitManagers name combination
            in the UnitNamesCombinationsManager.
        """
        dfs = {}
        for processing_combination in self.processing_combinations_data_manager.processing_combinations:
            outposts_manager = processing_combination.outposts_manager
            df = outposts_manager.compile_query_data_into_df()
            dfs[outposts_manager.name] = df
        return dfs
