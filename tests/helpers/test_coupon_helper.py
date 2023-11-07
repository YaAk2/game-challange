from helpers.coupon_helper import (
    get_num_of_pointees,
    get_max_coupon,
    remove_coupons,
    generate_coupons,
)
import pytest
from collections import defaultdict


@pytest.mark.parametrize(
    ["coupons", "cpos"],
    [
        pytest.param({(5, 5): [(5, 5), (5, 5)]}, (5, 5)),
        pytest.param({(5, 5): []}, (5, 5)),
        pytest.param({(5, 5): [(5, 5), (5, 5)]}, (6, 6)),
    ],
)
def test_get_num_of_pointees_returns_correct_num_of_pointees(coupons, cpos):
    n_pointees = get_num_of_pointees(coupons, cpos)

    assert n_pointees == len(coupons.get(cpos, []))


@pytest.mark.parametrize(
    ["coupons", "result"],
    [
        pytest.param({(5, 5): [(5, 5), (5, 5)], (6, 6): [(6, 6)]}, (5, 5)),
        pytest.param({(5, 5): [(5, 5), (5, 5)], (6, 6): []}, (5, 5)),
        pytest.param({(5, 5): [(5, 5)], (6, 6): [(6, 6)]}, (5, 5)),
        pytest.param({(5, 5): [], (6, 6): []}, (5, 5)),
        pytest.param({(5, 5): []}, (5, 5)),
    ],
)
def test_get_max_coupon_returns_coupon_with_max_pointees(coupons, result):
    coupon_max = get_max_coupon(coupons)

    assert coupon_max == result


@pytest.mark.parametrize(
    ["coupons", "cpos"],
    [
        pytest.param({(5, 5): [(5, 5), (5, 5)], (6, 6): [(6, 6)]}, [(5, 5)]),
        pytest.param({(5, 5): [(5, 5), (5, 5)], (6, 6): [(6, 6)]}, [(5, 5), (6, 6)]),
        pytest.param({}, [(5, 5)]),
        pytest.param({(5, 5): [(5, 5), (5, 5)]}, [()]),
        pytest.param({}, [()]),
    ],
)
def test_remove_coupons_deletes_coupons(coupons, cpos):
    coupon_reduced = remove_coupons(coupons, cpos)

    assert not all(coupon_reduced.get(c, False) for c in cpos)


@pytest.mark.parametrize(
    ["pointees", "result"],
    [
        pytest.param({(5, 5): [(6, 6)]}, {(6, 6): [(5, 5)]}),
        pytest.param({(5, 5): [(6, 6), (6, 6)]}, {(6, 6): [(5, 5), (5, 5)]}),
        pytest.param({(5, 5): [()]}, {(): [(5, 5)]}),
        pytest.param({(): [(5, 5)]}, {(5, 5): [()]}),
    ],
)
def test_generate_coupons_returns_coupons_with_correct_pointees(pointees, result):
    coupons = generate_coupons(pointees, defaultdict(list))

    assert coupons == result
