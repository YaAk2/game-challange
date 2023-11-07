from helpers.checkerboard_helper import draw_checkerboard
from helpers.coupon_helper import draw_coupons
from helpers.display_helper import display_text
from helpers.game.pointee import Pointee
from helpers.game.bird import Bird
from collections import defaultdict
import pygame


def refresh_screen(
    pnt: Pointee,
    pointees: defaultdict(list),
    coupons: defaultdict(list),
    bird: Bird,
    font: pygame.font.SysFont,
    settings: dict,
    rounds: int,
    max_coupon: tuple,
    n_pointees_collected: int,
) -> None:
    """
    The function updates and display the game screen .

    :param pnt: An instance of Pointee class
    :param pointees: A dictionary where the keys
    represent pointees and values coupons
    :param coupons: Contains the positions of
    the coupons and pointees
    :param bird: An instance of the bird class
    :param font: The font  object used for displaying
    text on the screen
    :param settings: Contains various settings for the game
    :param rounds: Current round number
    :param max_coupon: The coupon with the
    maximum number of pointees collected
    :param n_pointees_collected: The number of
    pointees that have been collected so far
    """
    pnt.screen.fill(settings["BACKGROUND_COLOR"])
    if (
        rounds % settings["REDEEM_COUPON_ROUND"] == 0
        and rounds > 0
        and rounds not in settings["SKIP_ROUNDS"]
    ):
        redeem_coupon_text = "Move your mouse to start the round."
        redeem_coupon_text2 = "Click on any coupon to collect the pointees."
        redeem_coupon_text3 = "OR If you are finished press ENTER."
        max_coupon_text = f"Coupon with maximum pointees: {str(max_coupon)}"
        n_pointees_collected_text = f"Collected pointees: {str(n_pointees_collected)}"
    else:
        redeem_coupon_text = ""
        redeem_coupon_text2 = ""
        redeem_coupon_text3 = ""
        max_coupon_text = ""
        n_pointees_collected_text = ""
    display_text(
        screen=pnt.screen,
        text=f"Round#: {str(rounds)}",
        font=font,
        color=settings["TEXT_COLOR"],
        pos=(0, 10),
    )
    display_text(
        screen=pnt.screen,
        text=redeem_coupon_text,
        font=font,
        color=settings["TEXT_COLOR"],
        pos=(0, 50),
    )
    display_text(
        screen=pnt.screen,
        text=redeem_coupon_text2,
        font=font,
        color=settings["TEXT_COLOR"],
        pos=(0, 65),
    )
    display_text(
        screen=pnt.screen,
        text=redeem_coupon_text3,
        font=font,
        color=settings["TEXT_COLOR"],
        pos=(0, 80),
    )
    display_text(
        screen=pnt.screen,
        text=max_coupon_text,
        font=font,
        color=settings["TEXT_COLOR"],
        pos=(0, 130),
    )
    display_text(
        screen=pnt.screen,
        text=n_pointees_collected_text,
        font=font,
        color=settings["TEXT_COLOR"],
        pos=(0, 170),
    )
    draw_checkerboard(
        pnt.screen,
        settings["GRID_COLOR"],
        settings["GRID_START_POS"],
        settings["GRID_SIZE"],
        settings["N_SQUARES"],
    )
    pnt.draw_pointees(pointees)
    draw_coupons(pnt.screen, coupons, font, settings["COUPON_COLOR"])
    bird.draw(pnt.screen)
    pygame.display.flip()
