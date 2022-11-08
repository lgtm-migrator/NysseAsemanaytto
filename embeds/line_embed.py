from __future__ import annotations
import datetime

import embeds
import digitransit.routing
import pygame

from core import render_info, logging, config
import digitransit.routing

class LineEmbed(embeds.Embed):
    def __init__(self, *args: str):
        self.line_index: int = 0
        self.active_lines: set[digitransit.routing.PatternGeometry]

    def on_enable(self):
        pass

    def on_disable(self):
        self.line_index += 1

    def render(self, surface: pygame.Surface, content_spacing: int, approx_datetime: datetime.datetime, progress: float):
        global last_render_cache_clear, line_render_cache_size

        surface_size: tuple[int, int] = surface.get_size()

        if last_render_cache_clear is None or (approx_datetime - last_render_cache_clear).days > 1:
            last_render_cache_clear = approx_datetime
            line_render_cache.clear()

        if line_render_cache_size is None or line_render_cache_size != surface_size:
            line_render_cache_size = surface_size
            line_render_cache.clear()

        lines = render_info.stopinfo.stoptimes
        assert lines is not None
        self.line_index %= len(lines)

        stoptime = lines[self.line_index]
        trip = stoptime.trip
        assert trip is not None

        if trip.patternCode not in line_render_cache:
            rendered: pygame.Surface | None = render_line_for_pattern(trip.patternCode, surface_size)
            if rendered is None:
                logging.error("Map line could not be rendered.")
            else:
                line_render_cache[trip.patternCode] = rendered

        surface.blit(line_render_cache[trip.patternCode], (0, 0))

    @staticmethod
    def name() -> str:
        return "lines"

    def requested_duration(self) -> float:
        return 15.0

last_render_cache_clear: datetime.datetime | None = None
line_render_cache_size: tuple[int, int] | None = None
line_render_cache: dict[str, pygame.Surface]

def render_line_for_pattern(patternCode: str, size: tuple[int, int]) -> pygame.Surface | None:
    pattern_geometry: digitransit.routing.PatternGeometry
    try:
        pattern_geometry = digitransit.routing.get_pattern_geometry(config.current.endpoint, patternCode)
    except Exception as e:
        logging.dump_exception(e, note="lineEmbed")
        return None


