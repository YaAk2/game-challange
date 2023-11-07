import random
import pygame
import math
from collections import defaultdict
from itertools import product
from numpy import arange


class Pointee:
    def __init__(
        self,
        screen: pygame.Surface,
        start: tuple,
        end: tuple,
        color: tuple,
        rad: int,
        distance: tuple,
    ) -> None:
        """
        The function initializes pointee object
        with various attributes.

        :param screen: Represents the screen on where
        the pointee object will be displayed
        :param start: Represents the starting position
        of the pointee objects
        :param end: Represents the coordinates of the end position
        :param color: Represents the color of pointee objects
        :param rad: The radius of pointee objects
        :param distance: Represents the distance
        between the pointee objects
        """
        self.screen = screen
        self.start = start
        self.end = end
        self.color = color
        self.rad = rad
        self.distance = distance

    def draw_pointees(
        self,
        pointees,
    ) -> None:
        """
        The function draws pointee objects on the screen.

        :param pointees: A dictionary where the keys
        represent pointees and values coupons
        """
        for ppos, _ in pointees.items():
            pygame.draw.circle(self.screen, self.color, ppos, self.rad)

    def __generate_point_randomly(self) -> tuple[defaultdict(list), defaultdict(list)]:
        """
        The function generates a random pointee.

        :return: A tuple containing two elements. The first
        element is the randomly generated position pos, and the
        second element is the converted position (ppos_to_cpos(pos))
        """
        pos: tuple = (
            random.randrange(
                int(self.start[0] + self.distance[0] / 2),
                self.start[0] + self.end[0],
                self.distance[0],
            ),
            random.randrange(
                int(self.start[1] + self.distance[1] / 2),
                self.start[1] + self.end[1],
                self.distance[1],
            ),
        )
        return (pos, self.ppos_to_cpos(pos))

    def generate_pointees_randomly(self, n: int) -> defaultdict(list):
        """
        The function generates a dictionary where the keys are
        randomly generated pointee positions and the
        values are lists of coupons position.

        :param n: Represents the number of
        pointees to generate randomly
        :return: A dictionary where the
        keys are pointee positions and
        the values are lists of coupon positions
        """
        pointees = defaultdict(list)
        for _ in range(n):
            ppos, cpos = self.__generate_point_randomly()
            pointees[ppos].append(cpos)
        return pointees

    def generate_pointees(self) -> defaultdict(list):
        """
        The function generates a dictionary where
        each key is a pointee and the
        corresponding value is a list of converted
        coordinates into coupons position.

        :return: The function returns a dictionary
        where the keys are pointee
        positions and the values are lists of
        corresponding coupon positions
        """
        pointees = defaultdict(list)
        ppos_x: list = list(
            arange(
                self.start[0] + self.distance[0] / 2,
                self.start[0] + self.end[0],
                self.distance[0],
            )
        )
        ppos_y: list = list(
            arange(
                self.start[1] + self.distance[1] / 2,
                self.start[1] + self.end[1],
                self.distance[1],
            )
        )
        ppos: list[tuple] = list(product(ppos_x, ppos_y))

        for p in ppos:
            pointees[p].append(self.ppos_to_cpos(p))
        return pointees

    def __correct_pos(self, x: float, y: float, ppos: tuple) -> tuple:
        """
        The function corrects the position (x, y) of a pointee.

        :param x: The x-coordinate of a pointee
        :param y: The current y-coordinate of a pointee
        :param ppos: Pointee pos to be corrected
        :return: a tuple containing the corrected
        x and y coordinates
        """
        if x > self.start[0] + self.end[0]:
            x = ppos[0]
        elif x < self.start[0]:
            x = self.start[0] + self.distance[0] / 2
        if y > self.start[1] + self.end[1]:
            y = ppos[1]
        elif y < self.start[1]:
            y = self.start[1] + self.distance[1] / 2
        return (x, y)

    def __jump(self, ppos: tuple) -> tuple:
        """
        The function randomly moves a pointee
        in a 2D space by a certain distance.

        :param ppos: Represents the current position of a pointee
        :return: A tuple containing the updated pointee and coupon
        """
        x: float = ppos[0] + random.choice([1, -1]) * self.distance[0]
        y: float = ppos[1] + random.choice([1, -1]) * self.distance[1]

        (x, y) = random.choice([(x, ppos[1]), (ppos[0], y), (x, y)])

        ppos = self.__correct_pos(x, y, ppos)

        cpos: tuple = self.ppos_to_cpos(ppos)
        return (ppos, cpos)

    def move_pointees(self, pointees: defaultdict(list)) -> defaultdict(list):
        """
        The function takes a dictionary of pointees and
        moves them to new positions based on __jump function.

        :param pointees: A dictionary where the keys
        represent pointees and values coupons
        :return: A dictionary where the keys are the
        positions of the pointees after moving, and the values
        are lists of the positions of coupons.
        """
        pointees_moved = defaultdict(list)
        for ppos, cpos in pointees.items():
            for _ in cpos:
                p, c = self.__jump(ppos)
                pointees_moved[p].append(c)
        return pointees_moved

    def ppos_to_cpos(self, ppos: tuple) -> tuple:
        """
        The function takes a position in a grid
        and converts it to a corresponding coupon position.

        :param ppos: Representing the position of the point
        :return: A tuple containing the x and y coordinates of the coupon
        """
        x: float = math.floor((ppos[0] - self.start[0]) / self.distance[0])
        y: float = math.floor((ppos[1] - self.start[1]) / self.distance[1])
        return (x, y)

    @staticmethod
    def remove_pointees(
        pointees: defaultdict(list), pointees_to_remove: list[tuple]
    ) -> defaultdict(list):
        """
        The function removes specified elements from pointees.

        :param pointees: A dictionary where the keys
        represent pointees and values coupons
        :param pointees_to_remove: A list of positions
        of pointees to be removed from the pointees
        :return: Updated pointees after removing the specified pointees.
        """
        for ppos in pointees_to_remove:
            pointees.pop(ppos, None)
        return pointees
