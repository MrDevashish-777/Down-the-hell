import pygame
from pygame.locals import RLEACCEL
import os
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT

def text_objects(text: str, font: pygame.font.Font, color: tuple) -> tuple:
    """
    Create a text surface and rectangle.

    Args:
        text (str): The text to render.
        font (pygame.font.Font): The font to use.
        color (tuple): The color of the text.

    Returns:
        tuple: A tuple containing the text surface and its rectangle.
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_display(game_display: pygame.Surface, text: str, x: int, y: int, font_size: int, color: tuple, centered_x: bool = False, centered_y: bool = False) -> None:
    """
    Display a message on the game display.

    Args:
        game_display (pygame.Surface): The surface to display the message on.
        text (str): The text to display.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        font_size (int): The size of the font.
        color (tuple): The color of the text.
        centered_x (bool): Whether to center the text horizontally. Defaults to False.
        centered_y (bool): Whether to center the text vertically. Defaults to False.

    Raises:
        ValueError: If any of the arguments are of the wrong type.
    """
    if not isinstance(game_display, pygame.Surface):
        raise ValueError("game_display must be a pygame Surface")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(x, (int, float)):
        raise ValueError("x must be a number")
    if not isinstance(y, (int, float)):
        raise ValueError("y must be a number")
    if not isinstance(font_size, int):
        raise ValueError("font_size must be an integer")
    if not isinstance(color, tuple) or len(color) != 3:
        raise ValueError("color must be a tuple of three integers")

    font = pygame.font.Font(None, font_size)
    text_surface, text_rect = text_objects(text, font, color)

    if centered_x and centered_y:
        text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    elif centered_x:
        text_rect.center = (SCREEN_WIDTH / 2, y)
    elif centered_y:
        text_rect.center = (x, SCREEN_HEIGHT / 2)
    else:
        text_rect.center = (x, y)

    game_display.blit(text_surface, text_rect)

def load_image(name: str, colorkey: tuple = None) -> pygame.Surface:
    """
    Load an image from the data directory.

    Args:
        name (str): The name of the image to load.
        colorkey (tuple): The colorkey to use. Defaults to None.

    Returns:
        pygame.Surface: The loaded image.

    Raises:
        SystemExit: If the image cannot be loaded.
    """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except (pygame.error, Exception) as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image