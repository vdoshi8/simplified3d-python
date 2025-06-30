import pytest
from logic.geometry import get_x, get_y, get_z


@pytest.mark.parametrize("line, expected", [
    ("G1 X10.5 Y20.0", 10.5),
    ("G1 X-5 Y3.1415", -5.0),
    ("G1 Xmissing", 0.0),
])
def test_get_x(line, expected):
    assert get_x(line) == expected


@pytest.mark.parametrize("line, expected", [
    ("G1 X0 Y15.25 F300", 15.25),
    ("G1 Y-2.5 Z5.0", -2.5),
    ("G1 Ymissing", 0.0),
])
def test_get_y(line, expected):
    assert get_y(line) == expected


@pytest.mark.parametrize("line, expected", [
    ("G1 X1 Y2 Z3.5", 3.5),
    ("G1 Z-1.25 E100", -1.25),
    ("G1 Zmissing", 0.0),
])
def test_get_z(line, expected):
    assert get_z(line) == expected

# ← make sure there’s exactly one newline below this line