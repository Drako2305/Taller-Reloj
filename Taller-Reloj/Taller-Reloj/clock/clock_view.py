"""Canvas that draws the analog clock face and its three hands."""

import math
import tkinter as tk
from typing import List, Optional, Tuple

from clock.clock_time import HandAngles
from clock.theme import Theme, blend

Point = Tuple[float, float]

CANVAS_SIZE = 560
BEZEL_RADIUS = 255
FACE_RADIUS = 232
TICK_OUTER_RADIUS = 214
MAJOR_TICK_INNER_RADIUS = 188
MINOR_TICK_INNER_RADIUS = 200
NUMERAL_RADIUS = 160
SHADOW_OFFSET = (4, 6)

STATIC_TAG = "static"
DYNAMIC_TAG = "dynamic"


class AnalogClockView(tk.Canvas):
    """Draws the dial once and redraws only the moving parts on every frame."""

    def __init__(self, master: tk.Misc, theme: Theme) -> None:
        super().__init__(
            master,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg=theme.background,
            highlightthickness=0,
        )
        self._theme = theme
        self._center = CANVAS_SIZE / 2
        self._draw_dial()

    # ------------------------------------------------------------------ dial

    def _draw_dial(self) -> None:
        self._draw_glow()
        self._draw_bezel()
        self._draw_face()
        self._draw_ticks()
        self._draw_numerals()
        self._draw_captions()

    def _draw_circle(self, radius: float, fill: str, tag: str = STATIC_TAG) -> None:
        c = self._center
        self.create_oval(
            c - radius, c - radius, c + radius, c + radius,
            fill=fill, outline="", tags=tag,
        )

    def _draw_glow(self) -> None:
        steps = 14
        for step in range(steps):
            radius = CANVAS_SIZE / 2 - step * 1.2
            ratio = (step / steps) ** 0.6
            color = blend(self._theme.background, self._theme.glow, ratio)
            self._draw_circle(radius, color)

    def _draw_bezel(self) -> None:
        self._draw_circle(BEZEL_RADIUS, self._theme.bezel_outer)
        self._draw_circle(BEZEL_RADIUS - 9, self._theme.bezel_inner)
        self._draw_circle(BEZEL_RADIUS - 13, self._theme.bezel_outer)

    def _draw_face(self) -> None:
        steps = 40
        for step in range(steps):
            radius = FACE_RADIUS * (1 - step / steps)
            ratio = step / (steps - 1)
            color = blend(self._theme.face_edge, self._theme.face_center, ratio)
            self._draw_circle(radius, color)

    def _draw_ticks(self) -> None:
        for index in range(60):
            is_major = index % 5 == 0
            inner = MAJOR_TICK_INNER_RADIUS if is_major else MINOR_TICK_INNER_RADIUS
            start = self._polar(inner, index * 6)
            end = self._polar(TICK_OUTER_RADIUS, index * 6)
            self.create_line(
                *start, *end,
                fill=self._theme.tick_major if is_major else self._theme.tick_minor,
                width=4 if is_major else 1.5,
                capstyle=tk.ROUND,
                tags=STATIC_TAG,
            )

    def _draw_numerals(self) -> None:
        for number in range(1, 13):
            x, y = self._polar(NUMERAL_RADIUS, number * 30)
            self.create_text(
                x, y,
                text=str(number),
                fill=self._theme.numeral,
                font=("Helvetica", 30, "bold"),
                tags=STATIC_TAG,
            )

    def _draw_captions(self) -> None:
        c = self._center
        self.create_text(
            c, c - 92,
            text="CIRCULAR DOUBLY LINKED LIST",
            fill=self._theme.caption,
            font=("Helvetica", 9, "bold"),
            tags=STATIC_TAG,
        )

    # --------------------------------------------------------------- hands

    def render(
        self,
        angles: HandAngles,
        date_text: str,
        next_alarm_text: Optional[str],
        ringing: bool,
        flash_on: bool,
    ) -> None:
        """Redraw everything that changes from one frame to the next."""
        self.delete(DYNAMIC_TAG)
        if ringing:
            self._draw_ringing_halo(flash_on)
        self._draw_information(date_text, next_alarm_text)
        self._draw_hand(angles.hour, length=120, width=11, tail=26, color=self._theme.hour_hand)
        self._draw_hand(angles.minute, length=178, width=8, tail=30, color=self._theme.minute_hand)
        self._draw_second_hand(angles.second)
        self._draw_center_cap()

    def _draw_ringing_halo(self, flash_on: bool) -> None:
        color = self._theme.ringing if flash_on else self._theme.accent
        c = self._center
        radius = BEZEL_RADIUS + 2
        self.create_oval(
            c - radius, c - radius, c + radius, c + radius,
            outline=color, width=8, tags=DYNAMIC_TAG,
        )

    def _draw_information(self, date_text: str, next_alarm_text: Optional[str]) -> None:
        c = self._center
        self.create_text(
            c, c + 92,
            text=date_text,
            fill=self._theme.numeral,
            font=("Helvetica", 13, "bold"),
            tags=DYNAMIC_TAG,
        )
        if next_alarm_text:
            self.create_text(
                c, c + 118,
                text=f"ALARM {next_alarm_text}",
                fill=self._theme.accent,
                font=("Helvetica", 11, "bold"),
                tags=DYNAMIC_TAG,
            )

    def _draw_hand(self, angle: float, length: float, width: float, tail: float, color: str) -> None:
        outline = self._hand_outline(angle, length, width, tail)
        shadow = [(x + SHADOW_OFFSET[0], y + SHADOW_OFFSET[1]) for x, y in outline]
        self.create_polygon(shadow, fill=self._theme.hand_shadow, outline="", tags=DYNAMIC_TAG)
        self.create_polygon(outline, fill=color, outline=color, width=1, tags=DYNAMIC_TAG)

    def _draw_second_hand(self, angle: float) -> None:
        color = self._theme.second_hand
        tip = self._polar(200, angle)
        tail = self._polar(-46, angle)
        weight = self._polar(-34, angle)
        self.create_line(
            tail[0] + SHADOW_OFFSET[0], tail[1] + SHADOW_OFFSET[1],
            tip[0] + SHADOW_OFFSET[0], tip[1] + SHADOW_OFFSET[1],
            fill=self._theme.hand_shadow, width=3, capstyle=tk.ROUND, tags=DYNAMIC_TAG,
        )
        self.create_line(*tail, *tip, fill=color, width=3, capstyle=tk.ROUND, tags=DYNAMIC_TAG)
        self.create_oval(
            weight[0] - 8, weight[1] - 8, weight[0] + 8, weight[1] + 8,
            fill=color, outline="", tags=DYNAMIC_TAG,
        )

    def _draw_center_cap(self) -> None:
        c = self._center
        for radius, color in (
            (13, self._theme.second_hand),
            (7, self._theme.bezel_outer),
            (3, self._theme.face_center),
        ):
            self.create_oval(
                c - radius, c - radius, c + radius, c + radius,
                fill=color, outline="", tags=DYNAMIC_TAG,
            )

    # ------------------------------------------------------------- geometry

    def _hand_outline(self, angle: float, length: float, width: float, tail: float) -> List[Point]:
        """Spear-shaped polygon for a hand pointing up, rotated by ``angle`` degrees."""
        local_points = [
            (0, -length),
            (width, -length * 0.22),
            (width * 0.55, tail),
            (-width * 0.55, tail),
            (-width, -length * 0.22),
        ]
        radians = math.radians(angle)
        cos, sin = math.cos(radians), math.sin(radians)
        return [
            (
                self._center + x * cos - y * sin,
                self._center + x * sin + y * cos,
            )
            for x, y in local_points
        ]

    def _polar(self, radius: float, angle: float) -> Point:
        """Point at ``radius`` from the center, ``angle`` degrees clockwise from 12."""
        radians = math.radians(angle)
        return (
            self._center + radius * math.sin(radians),
            self._center - radius * math.cos(radians),
        )
