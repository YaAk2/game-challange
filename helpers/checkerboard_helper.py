import pygame
from numpy import arange


def draw_checkerboard(
    screen: pygame.Surface, color: tuple, start: tuple, size: tuple, n_squares: tuple
) -> None:
    """
    The function draws a checkerboard pattern on the screen.

    :param screen: Represents the screen where
    the checkerboard will be drawn
    :param color: Color of the checkerboard squares
    :param start: Represents the starting position
    of the checkerboard on the screen
    :param size: Represents the size of the checkerboard
    :param n_squares: Represents the number of
    squares in each row and column of the checkerboard
    """
    n_squares_horizontal: int = int(size[0] / n_squares[0])
    n_squares_vertical: int = int(size[1] / n_squares[1])
    for x in arange(start[0], start[0] + size[0], n_squares_horizontal):
        for y in arange(start[1], start[1] + size[1], n_squares_vertical):
            rect = pygame.Rect(x, y, n_squares_horizontal, n_squares_vertical)
            pygame.draw.rect(screen, color, rect, 1)
