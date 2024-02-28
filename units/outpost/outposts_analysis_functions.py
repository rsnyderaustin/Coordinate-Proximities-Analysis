import numpy as np
import pandas as pd

from .outpost import Outpost


def now_scanning_outside_of_specified_range(distance, scan_range):
    return distance > scan_range


def sort_distances_to_scouts(distances: dict):
    return sorted(distances.items())


def is_number(variable_value):
    data_type = type(variable_value)
    return data_type == int or data_type == float or data_type == np.int64 or data_type == np.float64


def is_valid_value(value):
    return value and not pd.isna(value)


# Analysis functions:

def nearest_scout(outpost: Outpost) -> tuple:
    """

    :param outpost:
    :return: Tuple formatted (distance_to_closest_scout_hub, closest_scouts_data)
    """
    sorted_distances = outpost.get_sorted_distances_to_scouts()

    if not sorted_distances:
        return np.nan, ""

    distance_to_closest_scout_hub, closest_scouts_list = sorted_distances[0]
    closest_scouts_data = [scout.scout_data_map.data for scout in closest_scouts_list]
    return distance_to_closest_scout_hub, closest_scouts_data


def average_scouts_by_variable(outpost: Outpost, scan_range, variable):
    def determine_measure_avg(count, total_sum):
        if count == 0:
            return np.nan
        return float(total_sum) / count

    sorted_distances = outpost.get_sorted_distances_to_scouts()

    if not sorted_distances:
        return 0

    count = 0
    total_sum = 0

    for distance, scouts_at_same_distance in sorted_distances:
        if now_scanning_outside_of_specified_range(distance=distance,
                                                   scan_range=scan_range):
            return determine_measure_avg(count=count,
                                         total_sum=total_sum)
        for scout in scouts_at_same_distance:
            variable_value = scout.get_data(variable_name=variable)
            if not is_valid_value(variable_value):
                continue
            if not is_number(variable_value):
                raise Exception(f"Variable value '{variable_value}' is not expected type int or float for average "
                                f"function.")

            total_sum += variable_value
            count += 1

    # Reached end of function without exceeding specified scan_range, so fill units value with final result
    return determine_measure_avg(count=count,
                                 total_sum=total_sum)


def num_scouts_in_range(outpost: Outpost, scan_range):
    sorted_distances = outpost.get_sorted_distances_to_scouts()

    if not sorted_distances:
        return 0

    count = 0
    for distance, scout_list in sorted_distances:
        if now_scanning_outside_of_specified_range(distance, scan_range):
            return count
        else:
            count += len(scout_list)
    return count


def scout_in_range_tf(outpost: Outpost, scan_range):
    sorted_distances = outpost.get_sorted_distances_to_scouts()

    if not sorted_distances:
        return False

    closest_scout_hub = sorted_distances[0]
    closest_scout_hub_distance = closest_scout_hub[0]
    return closest_scout_hub_distance <= scan_range


def count_scouts_by_variable(outpost: Outpost, scan_range, variable, target_value):
    def scout_data_and_target_value_are_compatible_data_types(scout_value, target_value):
        if is_number(scout_value) and is_number(target_value):
            return True
        return isinstance(scout_value, type(target_value))

    sorted_distances = outpost.get_sorted_distances_to_scouts()

    if not sorted_distances:
        return 0

    count = 0

    for distance, scout_list in sorted_distances:
        if now_scanning_outside_of_specified_range(distance=distance,
                                                   scan_range=scan_range):
            return count
        for scout in scout_list:

            variable_value = scout.get_data(variable_name=variable)
            if not is_valid_value(variable_value):
                continue
            if not scout_data_and_target_value_are_compatible_data_types(scout_value=variable_value,
                                                                         target_value=target_value):
                raise TypeError(f"Variable value '{variable_value}' and target value '{target_value}' are"
                                f"incompatible.")

            if variable_value == target_value:
                count += 1

    # Reached end of function without exceeding specified scan_range, so return the final count
    return count
