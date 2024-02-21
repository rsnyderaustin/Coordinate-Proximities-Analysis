from geopy import Point
from geopy.distance import distance, geodesic


def create_bounding_box(center_coordinate, edge_distance):
    center_point = Point(center_coordinate[0], center_coordinate[1])
    north_point = distance(miles=edge_distance).destination(center_point, 0)
    south_point = distance(miles=edge_distance).destination(center_point, 180)
    east_point = distance(miles=edge_distance).destination(center_point, 90)
    west_point = distance(miles=edge_distance).destination(center_point, 270)

    left = west_point.longitude
    right = east_point.longitude
    bottom = south_point.latitude
    top = north_point.latitude

    bounding_box = (left, bottom, right, top)
    return bounding_box


def distance_between_points(coord1, coord2):
    return geodesic(coord1, coord2).miles


def coordinate_within_radius(reference_coordinate, center_coordinate, radius) -> tuple[bool, float]:
    points_distance = distance_between_points(center_coordinate, reference_coordinate)
    if points_distance <= radius:
        return True, points_distance
    else:
        return False, points_distance
