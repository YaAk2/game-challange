import pytest
from tests.conftest import SETTINGS, POINTEES_DISTANCE
import math


@pytest.mark.parametrize(
    ["n_pointees"],
    [
        pytest.param(0),
        pytest.param(10),
        pytest.param(10000),
    ],
)
def test_generate_pointees_randomly_returns_n_pointees(pnt, n_pointees):
    pointees = pnt.generate_pointees_randomly(n_pointees)

    assert len(sum(pointees.values(), [])) == n_pointees


def test_generate_pointees_randomly_returns_n_pointees_within_boundary(pnt):
    pointees = pnt.generate_pointees_randomly(1)
    ppos = list(pointees.keys())[0]

    assert (
        SETTINGS["GRID_START_POS"][0]
        <= ppos[0]
        <= SETTINGS["GRID_START_POS"][0] + SETTINGS["GRID_SIZE"][0]
    )
    assert (
        SETTINGS["GRID_START_POS"][1]
        <= ppos[1]
        <= SETTINGS["GRID_START_POS"][1] + SETTINGS["GRID_SIZE"][1]
    )


def test_generate_pointees_returns_correct_num_of_pointees(pnt):
    pointees = pnt.generate_pointees()

    assert len(pointees) == int(
        (SETTINGS["GRID_SIZE"][0] / POINTEES_DISTANCE[0])
    ) * int((SETTINGS["GRID_SIZE"][1] / POINTEES_DISTANCE[1]))


@pytest.mark.parametrize(
    ["pointees"],
    [
        pytest.param(
            {
                (
                    SETTINGS["GRID_START_POS"][0],
                    SETTINGS["GRID_START_POS"][1],
                ): []
            }
        ),
        pytest.param(
            {
                (
                    (
                        SETTINGS["GRID_SIZE"][0] / 2,
                        SETTINGS["GRID_SIZE"][1] / 2,
                    )
                ): []
            }
        ),
        pytest.param({SETTINGS["GRID_SIZE"]: []}),
    ],
)
def test_move_pointees_displaces_pointees(pnt, pointees):
    point_moved = pnt.move_pointees(pointees)

    assert pointees != point_moved


@pytest.mark.parametrize(
    ["pointees"],
    [
        pytest.param(
            {
                (
                    SETTINGS["GRID_START_POS"][0],
                    SETTINGS["GRID_START_POS"][1],
                ): [()]
            }
        ),
        pytest.param(
            {
                (
                    (
                        SETTINGS["GRID_SIZE"][0] / 2,
                        SETTINGS["GRID_SIZE"][0] / 2,
                    )
                ): [()]
            }
        ),
        pytest.param({SETTINGS["GRID_SIZE"]: [()]}),
    ],
)
def test_move_pointees_displaces_pointees_within_boundary(pnt, pointees):
    point_moved = pnt.move_pointees(pointees)
    ppos = list(point_moved.keys())[0]

    assert (
        SETTINGS["GRID_START_POS"][0]
        <= ppos[0]
        <= SETTINGS["GRID_START_POS"][0] + SETTINGS["GRID_SIZE"][0]
    )
    assert (
        SETTINGS["GRID_START_POS"][1]
        <= ppos[1]
        <= SETTINGS["GRID_START_POS"][1] + SETTINGS["GRID_SIZE"][1]
    )


@pytest.mark.parametrize(
    ["pointee"],
    [
        pytest.param((SETTINGS["GRID_START_POS"][0], SETTINGS["GRID_START_POS"][1])),
        pytest.param((SETTINGS["GRID_SIZE"][0] / 2, SETTINGS["GRID_SIZE"][0] / 2)),
        pytest.param(SETTINGS["GRID_SIZE"]),
    ],
)
def test_ppos_to_cpos_returns_correct_coupon_pos_given_pointee(pnt, pointee):
    cpos_x = math.floor(
        (pointee[0] - SETTINGS["GRID_START_POS"][0]) / POINTEES_DISTANCE[0]
    )
    cpos_y = math.floor(
        (pointee[1] - SETTINGS["GRID_START_POS"][1]) / POINTEES_DISTANCE[1]
    )
    cpos = pnt.ppos_to_cpos(pointee)

    assert cpos == (cpos_x, cpos_y)


@pytest.mark.parametrize(
    ["pointees", "pointees_to_remove", "result"],
    [
        pytest.param({(0, 0): []}, [(0, 0)], {}),
        pytest.param({(0, 0): [], (15, 15): []}, [(0, 0)], {(15, 15): []}),
    ],
)
def test_remove_pointees_drops_pointees(pnt, pointees, pointees_to_remove, result):
    pointees_reduced = pnt.remove_pointees(pointees, pointees_to_remove)
    assert pointees_reduced == result
