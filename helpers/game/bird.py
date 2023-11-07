import pygame
from numpy import clip
from random import choice
from collections import defaultdict


class Bird(pygame.sprite.Sprite):
    def __init__(
        self, size: tuple, pos: tuple, path_to_image: str, boundary: tuple
    ) -> None:
        """
        The function initializes a bird object.

        :param size: Desired size (width and height)
        of the bird object of the image in pixels
        :param pos: Initial position of the bird on the screen
        :param path_to_image: Path to the bird image
        :param boundary: Bird objects movement boundary
        """
        super().__init__()
        self.boundary = boundary
        self.image: pygame.Surface = pygame.image.load(path_to_image)
        self.image = pygame.transform.scale(self.image, size)
        self.rect: pygame.Rect = self.image.get_rect()
        self.set_pos(pos)
        self.keys = defaultdict()
        self.size = size

    def set_pos(self, pos: tuple) -> None:
        """
        The function sets the position of bird object.

        :param pos: Containing the x and y coordinates
        of the position the bird object should take
        """
        self.rect.x = clip(pos[0], self.boundary[0], self.boundary[2])
        self.rect.y = clip(pos[1], self.boundary[1], self.boundary[3])

    def __move_down(self, pxs: int) -> None:
        """
        The function moves the bird object
        down by a specified number of pixels.

        :param pxs: Represents the number of
        pixels to move the bird object down
        """
        self.rect.y = clip(
            self.rect.y + pxs, self.boundary[1], self.boundary[3] - self.size[1]
        )

    def __move_up(self, pxs: int) -> None:
        """
        The function moves the bird object up
        by a specified number of pixels.

        :param pxs: Represents the number of
        pixels to move the bird object upwards
        """
        self.rect.y = clip(self.rect.y - pxs, self.boundary[1], self.boundary[3])

    def __move_right(self, pxs: int) -> None:
        """
        The function moves the bird object to the
        right by a specified number of pixels.

        :param pxs: Represents the number of pixels
        to move the bird object to the right
        """
        self.rect.x = clip(
            self.rect.x + pxs, self.boundary[0], self.boundary[2] - self.size[0]
        )

    def __move_left(self, pxs: int) -> None:
        """
        The function moves the bird object to
        the left by a specified number of pixels.

        :param pxs: Represents the number of pixels
        by which the bird object should move to the left
        """
        self.rect.x = clip(self.rect.x - pxs, self.boundary[0], self.boundary[2])

    def __get_pressed_keys(self) -> None:
        """
        The function assigns the current state
        of all keyboard keys to the variable keys.
        """
        self.keys = pygame.key.get_pressed()

    def __generate_random_keys(self) -> None:
        """
        The function generates a dictionary of
        random boolean values for specific keys.
        """
        self.keys = {
            key: choice([False, True])
            for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
        }

    def move(
        self, dl: int, dr: int, du: int, dd: int, movement: str | None = "random"
    ) -> None:
        """
        The function maps keyboard keys to specific
        movements in a game.

        :param dl: Represents speed at which
        the bird object should move to the left
        :param dr: Represents speed at which the
        bird object shouldmove to the right
        :param du: Represents speed at which
        the bird object should move up
        :param dd: Represents speed at which
        the bird object should move down
        """
        if movement == "random":
            self.__generate_random_keys()
        else:
            self.__get_pressed_keys()
        if self.keys[pygame.K_UP]:
            self.__move_up(du)
        if self.keys[pygame.K_DOWN]:
            self.__move_down(dd)
        if self.keys[pygame.K_RIGHT]:
            self.__move_right(dr)
        if self.keys[pygame.K_LEFT]:
            self.__move_left(dl)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the bird object.

        :param screen: Represents the screen
        where the bird object will be drawn
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))
