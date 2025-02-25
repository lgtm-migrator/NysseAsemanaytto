from core.colors import Colors
from core import font_helper
import datetime
import pygame
import pygame.font
import pygame.surface

font: font_helper.SizedFont = font_helper.SizedFont("resources/fonts/Lato-Bold.ttf", "time rendering")

TIMEFORMAT = "%H:%M"

def render_time(px_height: int, time: datetime.time, color: tuple[int, int, int] = Colors.WHITE) -> pygame.Surface:
    global font
    timeStr = time.strftime(TIMEFORMAT)
    return font.get_size(px_height).render(timeStr, True, color)
