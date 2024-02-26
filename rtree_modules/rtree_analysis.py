from rtree import index

from . import spatial_analysis


class DistancesToCoordinatesMap:

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
        self.rtree = index.Index()

    def _get_coordinates_in_bounding_box(self, outpost_coordinate, scan_range) -> set[tuple]:
        bounding_box = spatial_analysis.create_bounding_box(center_coordinate=outpost_coordinate,
                                                            edge_distance=scan_range)
        rtree_objs_in_bounding_box = list(self.rtree.intersection(bounding_box, objects=True))
        coordinates = {(rtree_obj.bbox[1], rtree_obj.bbox[0]) for rtree_obj in rtree_objs_in_bounding_box}
        return coordinates

    def insert_coordinates_into_rtree(self, coordinates: list[tuple]):
        for i, scout_coordinate_tuple in enumerate(coordinates):
            latitude, longitude = scout_coordinate_tuple[0], scout_coordinate_tuple[1]
            self.rtree.insert(i, (longitude, latitude, longitude, latitude))

    def find_coordinates_around_point(self, reference_coordinate: tuple, scan_range: int) -> DistancesToCoordinatesMap:
        coordinates_in_bbox = self._get_coordinates_in_bounding_box(reference_coordinate, scan_range)

        distances_to_coordinates_map = DistancesToCoordinatesMap()
        # Within the bounding box doesn't mean within the circular radius
        for coordinate in coordinates_in_bbox:
            within_range, distance_result = spatial_analysis.coordinate_within_radius(
                reference_coordinate=coordinate,
                center_coordinate=reference_coordinate,
                radius=scan_range)
            if within_range:
                distances_to_coordinates_map.add_coordinate(coordinate=coordinate,
                                                            distance=distance_result)
        return distances_to_coordinates_map
