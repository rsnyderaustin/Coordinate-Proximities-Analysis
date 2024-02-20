from geopy import Point, distance
from rtree import index


class DistancesToCoordinates:

    def __init__(self):
        self.distances_to_coordinates = []
        self.processed_coordinates = set()

    def add_coordinate(self, coordinate, distance):
        if coordinate not in self.processed_coordinates:
            new_value = (coordinate, distance)
            self.distances_to_coordinates.append(new_value)
            self.processed_coordinates.add(coordinate)

    def coordinate_and_distance_generator(self):
        for coordinate, distance in self.distances_to_coordinates:
            yield coordinate, distance


class RtreeAnalyzer:

    def __init__(self):
        self.rtree = None

    @staticmethod
    def _create_bounding_box(coordinate, scan_range):
        center_point = Point(coordinate[0], coordinate[1])
        north_point = distance.distance(miles=scan_range).destination(center_point, 0)
        south_point = distance.distance(miles=scan_range).destination(center_point, 180)
        east_point = distance.distance(miles=scan_range).destination(center_point, 90)
        west_point = distance.distance(miles=scan_range).destination(center_point, 270)

        left = west_point.longitude
        right = east_point.longitude
        bottom = south_point.latitude
        top = north_point.latitude

        bounding_box = (left, bottom, right, top)
        return bounding_box

    @staticmethod
    def _distance_between(coord1, coord2):
        return distance.geodesic(coord1, coord2).miles

    def _get_scout_hubs_in_bounding_box(self, outpost_coordinate, scan_range):
        bounding_box = self._create_bounding_box(coordinate=outpost_coordinate,
                                                 scan_range=scan_range)
        scout_hubs_in_bbox = list(self.rtree.intersection(bounding_box, objects=True))
        return scout_hubs_in_bbox

    def _hub_within_exact_outpost_radius(self, scout_hub_coordinate, outpost_coordinate, scan_range):
        points_distance = self._distance_between(outpost_coordinate, scout_hub_coordinate)
        if points_distance <= scan_range:
            return points_distance
        else:
            return None

    def create_rtree(self, scout_coordinates: list[tuple]):
        rtree = index.Index()
        if not scout_coordinates:
            print("Method create_rtrees called on an empty set of scout coordinates.")

        for i, scout_coordinate_tuple in enumerate(scout_coordinates):
            latitude, longitude = scout_coordinate_tuple[0], scout_coordinate_tuple[1]
            rtree.insert(i, (longitude, latitude, longitude, latitude))
        self.rtree = rtree

    def scan_for_scouts_in_outpost_range(self, outpost_coordinate: tuple, scan_range: int) -> DistancesToCoordinates:
        scout_hubs_in_bbox = self._get_scout_hubs_in_bounding_box(outpost_coordinate, scan_range)

        distances_to_coordinates_obj = DistancesToCoordinates()
        # Within the bounding box doesn't mean within the circular radius
        for scout_hub in scout_hubs_in_bbox:
            scout_hub_coordinate = (scout_hub.bbox[1], scout_hub.bbox[0])
            distance_result = self._hub_within_exact_outpost_radius(scout_hub_coordinate, outpost_coordinate,
                                                                    scan_range)
            if distance_result:
                distances_to_coordinates_obj.add_coordinate(coordinate=scout_hub_coordinate,
                                                            distance=distance_result)
        return distances_to_coordinates_obj
