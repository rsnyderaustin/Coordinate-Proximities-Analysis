from environment_management.environment_manager import EnvironmentManager
from io_handling import unit_file

outpost_file = unit_file.UnitFile(
    file_alias='georgia_county_subs',
    latitude_column_name='INTPTLAT',
    longitude_column_name='INTPTLON',
    extra_column_names=['GISJOIN', 'U7H001'],
    file_path="C:/Users/austinsnyder/input_files/iowa_cty_subs.csv"
)
scout_file = unit_file.UnitFile(
    file_alias='georgia_fast_food',
    latitude_column_name='latitude',
    longitude_column_name='longitude',
    file_path="C:/Users/austinsnyder/input_files/iowa_fast_food.csv"
)
outpost_unit_files = {outpost_file}
scout_unit_files = {scout_file}
env_manager = EnvironmentManager(outpost_unit_files=outpost_unit_files,
                                 scout_unit_files=scout_unit_files)
env_manager.nearest_scout(scan_range=25)
env_manager.scout_in_range_tf(scan_range=25)
env_manager.num_scouts_in_range(scan_range=25)
env_manager.num_scouts_in_range_by_variable(scan_range=25,
                                            variable="name",
                                            target_value="McDonald's")
env_manager.num_scouts_in_range_by_variable(scan_range=25,
                                            variable="name",
                                            target_value="Taco Bell")
env_manager.process_analysis_functions()
env_manager.output_data_to_file(output_path="C:/Users/austinsnyder/output_files/georgia_analysis.xlsx")

