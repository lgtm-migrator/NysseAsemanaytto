from __future__ import annotations

import embeds
import digitransit.routing
import pygame

class LineEmbed(embeds.Embed):
    def __init__(self, *args: str):
        self.line_index: int = 0
        self.active_lines: set[digitransit.routing.PatternGeometry]

    def on_enable(self):
        pass

    def on_disable(self):
        self.line_index += 1

    def render(self, surface: pygame.Surface, content_spacing: int, progress: float):
        self.line_index %= len(filtered_alerts)
        alert = filtered_alerts[self.line_index]

    @staticmethod
    def name() -> str:
        return "lines"

    def requested_duration(self) -> float:
        return 15.0
