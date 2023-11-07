from helpers.coupon_helper import (
    generate_coupons,
    remove_coupons,
    get_num_of_pointees,
    get_max_coupon,
)
from helpers.game.pointee import Pointee
from helpers.game.bird import Bird
from collections import defaultdict
import pygame
from configs.logging import logging
import time


class GamePlay:
    def __init__(self, settings: dict, pnt: Pointee, bird: Bird) -> None:
        """
        The function initializes various attributes and
        variables for a game.

        :param settings: Contains various settings for the game
        :param pnt: An instance of class Pointee
        :param bird: An instance of class Bird
        """
        self.settings = settings
        self.pnt = pnt
        self.bird = bird
        self.rounds: int = 1
        self.n_pointees_collected_all: int = 0
        self.running: bool = True
        self.coupon_max: tuple = (None, None)

    def bird_approaches_checkerboard(
        self, pointees: defaultdict(list), coupons: defaultdict(list)
    ) -> tuple[defaultdict(list), defaultdict(list)]:
        """
        The function checks if a bird is approaching a
        checkerboard, moves pointees, generates coupons,
        resets the bird's position, and returns updated
        pointees and coupons.

        :param pointees: A dictionary where the
        keys represent pointees and values coupons
        :param coupons: Contains the positions
        of the coupons and pointees positions
        :return: pointees and coupons
        """
        if self.__is_pointees_collectable():
            self.bird.set_pos(self.settings["BIRD_START_POS"])
            self.bird.move(0, 0, 0, 0, "random")
        else:
            self.bird.move(
                self.settings["BIRD_SPEED"][0],
                self.settings["BIRD_SPEED"][1],
                self.settings["BIRD_SPEED"][2],
                self.settings["BIRD_SPEED"][3],
                self.settings["BIRD_MOVEMENT"],
            )
        if (
            self.bird.rect.x
            < self.settings["GRID_SIZE"][0] + self.settings["GRID_START_POS"][0]
            and self.bird.rect.x
            > self.settings["GRID_START_POS"][0] - self.settings["BIRD_SIZE"][0]
            and self.bird.rect.y
            < self.settings["GRID_SIZE"][1] + self.settings["GRID_START_POS"][1]
            and self.bird.rect.y
            > self.settings["GRID_START_POS"][1] - self.settings["BIRD_SIZE"][1]
        ):
            pointees = self.pnt.move_pointees(pointees)
            coupons = generate_coupons(pointees, defaultdict(list))

            self.bird.set_pos(self.settings["BIRD_START_POS"])

            self.__increment_rounds()

        return pointees, coupons

    def __player_can_redeem_coupons(
        self, pointees: defaultdict(list), coupons: defaultdict(list)
    ) -> tuple[defaultdict(list), defaultdict(list)]:
        """
        The function allows a player to redeem coupons.

        :param pointees: A dictionary where the keys
        represent pointees and values coupons
        :param coupons: Contains the positions
        of the coupons and pointees positions
        :return: pointees and coupons
        """
        pos_clicked: tuple = pygame.mouse.get_pos()
        coupon_clicked: tuple = self.pnt.ppos_to_cpos(pos_clicked)

        n_pointees_collected: int = get_num_of_pointees(coupons, coupon_clicked)
        self.n_pointees_collected_all += n_pointees_collected
        if n_pointees_collected != 0:
            pointees_to_remove: tuple = coupons.get(coupon_clicked, [])
            pointees = self.pnt.remove_pointees(pointees, pointees_to_remove)
        else:
            logging.warning("This coupon contains no pointees!")
        coupons = remove_coupons(coupons, [coupon_clicked])

        return pointees, coupons

    def translate_events(
        self, pointees: defaultdict(list), coupons: defaultdict(list)
    ) -> tuple[defaultdict(list), defaultdict(list)]:
        """
        The function handles various events in a round.

        :param pointees: A dictionary where the keys
        represent pointees and values coupons
        :param coupons: Contains the positions
        of the coupons and pointees positions
        :return: pointees and coupons
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.__is_pointees_collectable():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__increment_rounds()
                if event.type == pygame.MOUSEBUTTONUP:
                    pointees, coupons = self.__player_can_redeem_coupons(
                        pointees, coupons
                    )
                if not coupons:
                    self.coupon_max = (None, None)
                    logging.info("No coupons left!")
                    self.__init_end_level()
                    break
                self.coupon_max = get_max_coupon(coupons)
            else:
                self.coupon_max = (None, None)
        return pointees, coupons

    def __is_pointees_collectable(self) -> bool:
        """
        The function checks if the current round is
        eligible for collecting pointees.
        :return: A boolean value
        """
        return (
            self.rounds % self.settings["REDEEM_COUPON_ROUND"] == 0
            and self.rounds > 0
            and self.rounds not in self.settings["SKIP_ROUNDS"]
        )

    def __init_end_level(self) -> None:
        """
        The function logs the number of pointees collected
        and sets the running variable to False.
        """
        logging.info(f"Pointees collected: {self.n_pointees_collected_all}")
        self.running = False

    def end_game(self) -> None:
        """
        The function ends the game.
        """
        logging.info("Reached end of Game!")
        time.sleep(3)
        self.__init_end_level()

    def __increment_rounds(self) -> None:
        """
        The function increments the number of rounds and
        checks if the current round is the end round.
        """
        self.rounds += 1
        if self.rounds == self.settings["END_ROUND"]:
            self.end_game()
