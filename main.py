import yaml
import pygame
from helpers.game.pointee import Pointee
from helpers.game.gameplay import GamePlay
from helpers.coupon_helper import (
    generate_coupons,
)
from helpers.game.bird import Bird
from helpers.screen_helper import refresh_screen
from collections import defaultdict

from configs.font import font

# settings
with open("configs/game_settings.yaml", "r") as f:
    SETTINGS = yaml.load(f.read(), Loader=yaml.FullLoader)


def main():
    # init screen
    pygame.init()
    screen = pygame.display.set_mode(SETTINGS["SCREEN_SIZE"])
    screen.fill(SETTINGS["BACKGROUND_COLOR"])

    # init game objects
    bird = Bird(
        SETTINGS["BIRD_SIZE"],
        SETTINGS["BIRD_START_POS"],
        SETTINGS["BIRD_PATH_TO_IMAGE"],
        (0, 0, SETTINGS["SCREEN_SIZE"][0], SETTINGS["SCREEN_SIZE"][1]),
    )

    pointees_distance: tuple = (
        (SETTINGS["GRID_SIZE"][0] / SETTINGS["N_SQUARES"][0]),
        (SETTINGS["GRID_SIZE"][1] / SETTINGS["N_SQUARES"][1]),
    )
    pnt = Pointee(
        screen,
        SETTINGS["GRID_START_POS"],
        SETTINGS["GRID_SIZE"],
        SETTINGS["POINTEES_COLOR"],
        SETTINGS["POINTEES_RADIUS"],
        pointees_distance,
    )

    # generate init pointees and coupons
    pointees = pnt.generate_pointees()
    coupons = generate_coupons(pointees, defaultdict(list))

    # init game play
    game = GamePlay(SETTINGS, pnt, bird)

    # gameplay loop
    clock = pygame.time.Clock()
    while game.running:
        pointees, coupons = game.bird_approaches_checkerboard(pointees, coupons)

        pointees, coupons = game.translate_events(pointees, coupons)

        refresh_screen(
            pnt,
            pointees,
            coupons,
            bird,
            font,
            SETTINGS,
            game.rounds,
            game.coupon_max,
            game.n_pointees_collected_all,
        )

        clock.tick(SETTINGS["FPS"])
    pygame.quit()


if __name__ == "__main__":
    main()
