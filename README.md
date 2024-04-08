### Project Description
Analyze the qualities of one set of coordinates around a second set of coordinates. Throughout the program code and this description, the primary coordinate set is referred to as 'Outposts', and the secondary set are referred to as 'Scouts'. The naming scheme is intended to provide clarity on the relationship between the two, which is that Outposts individually keep track of and analyze the Scouts surrounding them. For example, if you wanted to analyze revenue of restaurants around different cities, the restaurants would be Scouts and the cities would be Outposts. Each Outpost is analyzed independent of one another, so there is no need to regard any overlap of Outposts analyses. 

### Project Implementation
The overall program is managed through the EnvironmentManager class, which takes UnitFile class objects as input. The code below provides an example of initializing an EnvironmentManager:

```
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
```

Column names included in the 'extra_column_names' parameter are included in the final data output for each outpost. For instance, in our previous example analysis of restaurants around cities, we might include the city populations, average population age, etc. Those values for each city would then be pulled straight from the original file and exported alongside our analysis data, allowing for more intricate analyses. 

If multiple Outpost UnitFile and/or multiple Scout UnitFile objects are passed into EnvironmentManager, each individual Outpost UnitFile dataset will be analyzed against all Scout UnitFile data **collectively**. See the example below:

```
outpost_unit_files = {A, B, C}
scout_unit_files = {Y, X, Z}
```

results in analysis combinations:
* A: (Y, X, Z)
* B: (Y, X, Z)
* C: (Y, X, Z)

So, in this example, for the analysis of each individual Outpost UnitFile dataset, the coordinates data in Scout UnitFile's Y, X, and Z are combined and analyzed as one whole.

Coordinate analysis functions are called on the EnvironmentManager object. The available analyis functions are listed below:
* **scout_in_range_tf** - For each outpost, determine whether a scout is within the provided distance range.
* **num_scouts_in_range** - For each outpost, determine the number of scouts within the provided distance range.
* **num_scouts_in_range_by_variable** - For each outpost, determine the number of scouts within the provided distance range that have a specific value for a specific variable. For example, number of restaurants with a value of "Fast Food" for variable "Type Food Served" around each city, for a set of cities.
* **average_scouts_by_variable** - For each otupost, determine the average value for a certain variable of scouts in the provided distance range. For example, average revenue of restaurants around each city, for a set of cities.
* **nearest_scout** - For each outpost, determine the nearest scout in the provided distance range.

Analysis functions are called lazily, meaning each analysis function call adds to a function stack until process_analysis_functions() is called on EnvironmentManager. Function output_data_to_file() loads the Outpost coordinates, analysis function results, and Outpost extra_column_names into either an Excel or CSV file, depending on the user-specified output path. The code below provides an example of calling analysis functions, followed by calling of process_analysis_functions() and output_data_to_file() on the Environment Manager.

```
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
```
### Questions, Contributions, and Feedback
If you would like to ask questions, provide any feedback, or contribute to the project, please feel free to do so. You may also contact me via email at rsnyder.austin@gmail.com.
