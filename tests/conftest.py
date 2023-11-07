import pytest
from helpers.game.pointee import Pointee
from helpers.game.bird import Bird
from helpers.game.gameplay import GamePlay
from pytest import MonkeyPatch
import pygame
import yaml

DUMMY_POINTEES = {(500, 500): [500, 500]}
DUMMY_COUPONS = {(500, 500): [500, 500]}

with open("tests/test_game_settings.yaml", "r") as f:
    SETTINGS = yaml.load(f.read(), Loader=yaml.FullLoader)

POINTEES_DISTANCE: tuple = (
    (SETTINGS["GRID_SIZE"][0] / SETTINGS["N_SQUARES"][0]),
    (SETTINGS["GRID_SIZE"][1] / SETTINGS["N_SQUARES"][1]),
)


class RectMock:
    def __init__(self, path_to_image: str) -> None:
        """
        The initializes the x and y coordinates to 0.

        :param path_to_image: Rrepresents the file path to an image.
        """
        self.x = 0
        self.y = 0

    def get_rect(self):
        """
        The function `get_rect` returns the current instance of the RectMock class.
        """
        return self


@pytest.fixture
def pnt():
    pnt = Pointee(
        None,
        SETTINGS["GRID_START_POS"],
        SETTINGS["GRID_SIZE"],
        SETTINGS["POINTEES_COLOR"],
        SETTINGS["POINTEES_RADIUS"],
        POINTEES_DISTANCE,
    )
    yield pnt


@pytest.fixture
def bird():
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(
        "pygame.image.load",
        RectMock,
    )
    monkeypatch.setattr(
        pygame.transform,
        "scale",
        lambda x, y: x,
    )
    bird = Bird(
        SETTINGS["BIRD_SIZE"],
        SETTINGS["BIRD_START_POS"],
        SETTINGS["BIRD_PATH_TO_IMAGE"],
        (0, 0, SETTINGS["SCREEN_SIZE"][0], SETTINGS["SCREEN_SIZE"][1]),
    )
    yield bird


@pytest.fixture
def game(pnt, bird):
    game = GamePlay(SETTINGS, pnt, bird)
    yield game


@pytest.fixture
def pygame_init():
    pygame.init()
    yield
