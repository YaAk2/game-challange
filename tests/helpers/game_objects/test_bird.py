from tests.conftest import SETTINGS
from pytest import MonkeyPatch
import pytest
import pygame


def test_set_pos_moves_bird_to_given_pos(bird):
    pos = (15, 15)
    bird.set_pos(pos)

    assert (bird.rect.x, bird.rect.y) == pos


@pytest.mark.parametrize(
    ["keys", "pxs", "result"],
    [
        pytest.param(
            {1073741906: True, 1073741905: False, 1073741903: False, 1073741904: False},
            (10, 10, 10, 10),
            (
                SETTINGS["BIRD_START_POS"][0],
                SETTINGS["BIRD_START_POS"][1] - 10,
            ),
        ),
        pytest.param(
            {1073741906: False, 1073741905: True, 1073741903: False, 1073741904: False},
            (10, 10, 10, 10),
            (
                SETTINGS["BIRD_START_POS"][0],
                SETTINGS["BIRD_START_POS"][1] + 10,
            ),
        ),
        pytest.param(
            {1073741906: False, 1073741905: False, 1073741903: True, 1073741904: False},
            (10, 10, 10, 10),
            (
                SETTINGS["BIRD_START_POS"][0] + 10,
                SETTINGS["BIRD_START_POS"][1],
            ),
        ),
        pytest.param(
            {1073741906: False, 1073741905: False, 1073741903: False, 1073741904: True},
            (10, 10, 10, 10),
            (
                SETTINGS["BIRD_START_POS"][0] - 10,
                SETTINGS["BIRD_START_POS"][1],
            ),
        ),
    ],
)
def test_move_handles_keys_correctly(bird, keys, pxs, result):
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: keys,
    )

    bird.move(pxs[0], pxs[1], pxs[2], pxs[3], "controllable")
    pos_curr = (bird.rect.x, bird.rect.y)

    assert pos_curr == result
