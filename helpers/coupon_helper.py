from collections import defaultdict
from helpers.display_helper import display_text
import pygame


def draw_coupons(
    screen: pygame.Surface,
    coupons: defaultdict(list),
    font: pygame.font.SysFont,
    color: tuple,
) -> None:
    """
    The function displays the number of pointees in coupons.

    :param screen: Represents the screen where
    the number of pointees will be drawn
    :param coupons: Contains the positions of
    the coupons and pointees
    :param font: Is the font object that will
    be used to render the text on the screen
    :param color: The color that will be
    used to draw the text on the screen
    """
    for cpos, ppos in coupons.items():
        display_text(
            screen=screen, text=str(len(ppos)), font=font, color=color, pos=ppos[0]
        )


def get_num_of_pointees(coupons: defaultdict(list), cpos: tuple) -> int:
    """
    The function returns the number of pointees for a given coupon.

    :param coupons: Contains the positions
    of the coupons and pointees
    :param cpos: Represents the position of a coupon
    :return: The number of pointees associated
    with the given coupon
    """
    n_pointees = len(coupons.get(cpos, []))
    return n_pointees


def get_max_coupon(coupons: defaultdict(list)) -> tuple:
    """
    The function returns the position of the
    coupon with the maximum number of pointees.

    :param coupons: Contains the positions of
    the coupons and pointees
    :return: Coupon with the maximum number of pointees
    """
    coupon_max = max(coupons.items(), key=lambda v: len(v[1]))[0]
    return coupon_max


def remove_coupons(
    coupons: defaultdict(list), coupons_to_remove: list[tuple]
) -> defaultdict(list):
    """
    The function removes specified coupons.

    :param coupons: Contains the positions
    of the coupons and number of pointees
    :param coupons_to_remove: A list of coupons to be removed
    :return: The updated coupons after
    removing the specified coupons.
    """
    for cpos in coupons_to_remove:
        coupons.pop(cpos, None)
    return coupons


def generate_coupons(
    pointees: defaultdict(list), coupons=defaultdict(list)
) -> defaultdict(list):
    """
    The function generates coupons associated
    with the corresponding pointees.

    :param pointees: A dictionary where the keys
    represent pointees and values coupons
    :param coupons: Contains the positions of
    the coupons and pointees
    :return: A dictionary of coupons, where the keys
    are coupon positions and the values are lists of
    pointee positions
    """
    for ppos, cpos in pointees.items():
        for c in cpos:
            coupons[c].append(ppos)
    return coupons
