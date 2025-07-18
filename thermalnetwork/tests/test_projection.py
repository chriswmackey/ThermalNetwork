from unittest import TestCase

import pytest

from thermalnetwork.geometry import polygon_area
from thermalnetwork.projection import lon_lat_to_polygon, meters_to_long_lat_factors, polygon_to_lon_lat


class TestProjection(TestCase):
    def test_meters_to_long_lat_factors(self):
        """Test the meters_to_long_lat_factors method."""
        assert meters_to_long_lat_factors((0, 0))[0] == pytest.approx(111319.9, rel=1e-5)
        assert meters_to_long_lat_factors((0, 0))[1] == pytest.approx(111319.9, rel=1e-5)

        assert meters_to_long_lat_factors((0, 45))[0] < meters_to_long_lat_factors((0, 45))[1] < 111319.9

        assert meters_to_long_lat_factors((0, 89))[0] < meters_to_long_lat_factors((0, 89))[1] < 111319.9

    def test_lon_lat_to_polygon(self):
        """Test conversion of lon lat to model units"""

        polygon_lon_lat_coords = [
            (-70.0, 42.0),
            (-69.99997578750273, 42.0),
            (-69.99997578750273, 42.00001799339205),
            (-70.0, 42.00001799339205),
        ]

        polygon = lon_lat_to_polygon(polygon_lon_lat_coords, origin_lon_lat=(-70.0, 42.0))

        test_polygon = [(0, 0), (2, 0), (2, 2), (0, 2)]

        # Check length
        assert len(test_polygon) == len(polygon)

        # Check coordinate values
        for point, test_point in zip(polygon, test_polygon):
            assert test_point[0] == pytest.approx(point[0], abs=1e-5)
            assert test_point[1] == pytest.approx(point[1], abs=1e-5)

        # check the area
        assert polygon_area(polygon) == pytest.approx(4.0, abs=1e-5)

    def test_polygon_to_lon_lat(self):
        """Test the polygon_to_lon_lat method."""
        polygon = ((0, 0), (2, 0), (2, 2), (0, 2))
        lat = 42.0
        lon = -70.0
        verts1 = polygon_to_lon_lat(polygon, (lon, lat))

        assert len(verts1) == 4
        for vert in verts1:
            assert vert[0] == pytest.approx(lon, rel=1e-5)
            assert vert[1] == pytest.approx(lat, rel=1e-5)

        convert_facs = meters_to_long_lat_factors((lon, lat))
        verts2 = polygon_to_lon_lat(polygon, (lon, lat), convert_facs)

        for vert1, verts2 in zip(verts1, verts2):
            assert vert1 == verts2
