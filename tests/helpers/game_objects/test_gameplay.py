import pytest
import pygame
from tests.conftest import DUMMY_COUPONS, DUMMY_POINTEES, SETTINGS
from pytest import MonkeyPatch
import time


def test_bird_approaches_checkerboard_and_freezes(bird, game):
    game.rounds = SETTINGS["REDEEM_COUPON_ROUND"]
    _, _ = game.bird_approaches_checkerboard(DUMMY_POINTEES, DUMMY_COUPONS)

    assert (bird.rect.x, bird.rect.y) == SETTINGS["BIRD_START_POS"]


@pytest.mark.parametrize(
    ["bird_pos"],
    [
        pytest.param(
            (
                SETTINGS["GRID_SIZE"][0]
                + SETTINGS["GRID_START_POS"][0]
                - SETTINGS["BIRD_SIZE"][0],
                SETTINGS["GRID_SIZE"][1]
                + SETTINGS["GRID_START_POS"][1]
                - SETTINGS["BIRD_SIZE"][1],
            )
        ),
        pytest.param(
            (
                SETTINGS["GRID_START_POS"][0] + SETTINGS["BIRD_SIZE"][0],
                SETTINGS["GRID_START_POS"][1] + SETTINGS["BIRD_SIZE"][1],
            )
        ),
    ],
)
def test_bird_approaches_checkerboard_and_pointees_move(bird, game, bird_pos):
    bird.rect.x = bird_pos[0]
    bird.rect.y = bird_pos[1]

    pointees, coupons = game.bird_approaches_checkerboard(DUMMY_POINTEES, DUMMY_COUPONS)

    assert pointees != DUMMY_POINTEES
    assert coupons != DUMMY_COUPONS


def test_bird_approaches_checkerboard_increments_round(bird, game):
    bird.rect.x = SETTINGS["GRID_START_POS"][0] + SETTINGS["BIRD_SIZE"][0]
    bird.rect.y = SETTINGS["GRID_START_POS"][1] + SETTINGS["BIRD_SIZE"][1]

    _, _ = game.bird_approaches_checkerboard(DUMMY_POINTEES, DUMMY_COUPONS)

    assert game.rounds == 2


def test_translate_events_handles_quitting_game(game, pygame_init):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    _, _ = game.translate_events(DUMMY_POINTEES, DUMMY_COUPONS)

    assert game.running is False


def test_translate_events_handles_pressing_enter(game, pygame_init):
    pygame.event.post(pygame.event.Event(pygame.K_RETURN, key=pygame.KEYDOWN))
    game.rounds = SETTINGS["REDEEM_COUPON_ROUND"]
    _, _ = game.translate_events(DUMMY_POINTEES, DUMMY_COUPONS)

    assert game.rounds > 0


def test_translate_events_handles_not_clicking_on_coupon(game, pygame_init):
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP))
    mouse_pos = next(iter(DUMMY_COUPONS.keys()))
    game.rounds = SETTINGS["REDEEM_COUPON_ROUND"]
    _, coupons = game.translate_events(DUMMY_POINTEES, DUMMY_COUPONS)

    assert coupons.get(mouse_pos, False)


@pytest.mark.skip(reason="Setting the mouse position does not work.")
def test_translate_events_handles_clicking_on_coupon(game, pygame_init):
    mouse_pos = next(iter(DUMMY_COUPONS.keys()))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP))
    pygame.mouse.set_pos(mouse_pos[0], mouse_pos[1])
    game.rounds = SETTINGS["REDEEM_COUPON_ROUND"]
    _, coupons = game.translate_events(DUMMY_POINTEES, DUMMY_COUPONS)

    assert not coupons.get(mouse_pos, False)
    assert game.n_pointees_collected_all == 1


def test_translate_events_handles_quits_game_if_coupons_empty(game, pygame_init):
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP))
    game.rounds = SETTINGS["REDEEM_COUPON_ROUND"]
    _, _ = game.translate_events({}, {})

    assert game.running is False


def test_end_game_quits_game(game):
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(
        time,
        "sleep",
        lambda x: None,
    )
    game.end_game()
    assert game.running is False
