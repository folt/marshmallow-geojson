"""Utility functions for tests."""


def assert_coordinates_equal(coord, expected):
    """Assert that coordinates match expected [lon, lat] or [lon, lat, alt].

    Args:
        coord: Coordinate value (can be tuple, list, or dict).
        expected: Expected coordinate list [lon, lat] or [lon, lat, alt].
    """
    if isinstance(coord, (tuple, list)):
        assert len(coord) >= 2
        assert coord[0] == expected[0], f"Longitude mismatch: {coord[0]} != {expected[0]}"
        assert coord[1] == expected[1], f"Latitude mismatch: {coord[1]} != {expected[1]}"
        if len(expected) > 2:
            assert len(coord) >= 3, "Expected altitude but coordinate has only 2 elements"
            assert coord[2] == expected[2], f"Altitude mismatch: {coord[2]} != {expected[2]}"
    else:
        # Handle dict format if needed
        assert coord == expected
