from coordinate_proximities_analysis.coordinate_proximities_analyzer import CoordinateProximitiesAnalyzer
from io_handling import unit_file

outpost_file = unit_file.UnitFile(
    file_alias='georgia_county_subs',
    latitude_column_name='INTPTLAT',
    longitude_column_name='INTPTLON',
    extra_column_names={'GISJOIN', 'U7H001'},
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
cpa = CoordinateProximitiesAnalyzer(outpost_unit_files=outpost_unit_files,
                                    scout_unit_files=scout_unit_files,
                                    self_comparison=True)
cpa.nearest_scout(scan_range=25)
cpa.scout_in_range_true_false(scan_range=25)
cpa.number_of_scouts_in_range(scan_range=25)
cpa.number_of_scouts_in_range_by_variable(scan_range=25,
                                          variable_name="name",
                                          target_value="McDonald's")
cpa.number_of_scouts_in_range_by_variable(scan_range=25,
                                          variable_name="name",
                                          target_value="Taco Bell")

cpa.process_analysis_functions(output_file_path="C:/Users/austisnyder/outputs/sample_output.xlsx")
