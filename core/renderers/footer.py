import pygame
import pygame.image
import pygame.font
import pygame.surface
import pygame.transform
from core.colors import Colors
from core import logging

nyssefi_font_height: int | None = None
nyssefi_text: pygame.Surface | None = None

footer_pictograms: pygame.Surface | None = None

cached_footer: pygame.Surface | None = None

def _render_footer_internal(px_size: tuple[int, int]) -> pygame.Surface:
    global nyssefi_font_height, footer_pictograms, nyssefi_text
    target_nyysefi_font_height: int = px_size[1]
    if nyssefi_text is None or target_nyysefi_font_height != nyssefi_font_height:
        logging.debug("Loading new 'nysse.fi' for stop info rendering...", stack_info=False)
        nyssefi_font_height = target_nyysefi_font_height
        nyssefi_font = pygame.font.Font("resources/fonts/Lota-Grotesque-Bold.otf", nyssefi_font_height)
        nyssefi_text = nyssefi_font.render("nysse.fi", True, Colors.WHITE)

    footer_pictograms_height: float = px_size[1] * 0.7
    if footer_pictograms is None or footer_pictograms.get_height() != round(footer_pictograms_height):
        logging.debug("Loading new pictograms for footer...", stack_info=False)
        footer_pictograms = pygame.image.load("resources/textures/elements/footer/footer_pictograms.png")
        footer_pictograms_width: float = footer_pictograms.get_width() / footer_pictograms.get_height() * footer_pictograms_height
        footer_pictograms = pygame.transform.smoothscale(footer_pictograms, (round(footer_pictograms_width), round(footer_pictograms_height))).convert_alpha()

    surf = pygame.Surface(px_size, pygame.SRCALPHA)

    pictograms_x = px_size[0] - footer_pictograms.get_width()
    surf.blit(footer_pictograms, (pictograms_x, px_size[1] // 2 - footer_pictograms.get_height() // 2))

    surf.blit(nyssefi_text, (pictograms_x - (nyssefi_text.get_width() // 5 * 0.7) - nyssefi_text.get_width(), px_size[1] // 2 - nyssefi_text.get_height() // 2))

    return surf

def render_footer(px_size: tuple[int, int]) -> pygame.Surface:
    global cached_footer
    if cached_footer is None or cached_footer.get_size() != px_size:
        logging.debug("Rendering new footer...", stack_info=False)
        cached_footer = _render_footer_internal(px_size)

    return cached_footer
