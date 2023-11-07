import pygame


def display_text(
    *,
    screen: pygame.Surface,
    text: str,
    font: pygame.font.SysFont,
    color: tuple,
    pos: tuple
) -> None:
    """
    The function displays the text on the screen.

    :param screen: Represents the screen
    where the text will be drawn
    :param text: A string to display on the screen
    :param font: Is the font object that will
    be used to render the text on the screen
    :param color: The color that will be used
    to draw the text on the screen
    :param pos: Represents the position where
    the text will be displayed
    """
    text_surface: pygame.Surface = font.render(text, False, color)
    screen.blit(text_surface, pos)
