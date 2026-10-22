"""Colors of the application and a helper to blend them."""

from dataclasses import dataclass


def blend(color_a: str, color_b: str, ratio: float) -> str:
    """Mix two ``#rrggbb`` colors. ``ratio`` 0 gives ``color_a`` and 1 gives ``color_b``."""
    channels_a = [int(color_a[i : i + 2], 16) for i in (1, 3, 5)]
    channels_b = [int(color_b[i : i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(a + (b - a) * ratio) for a, b in zip(channels_a, channels_b)]
    return "#{:02x}{:02x}{:02x}".format(*mixed)


@dataclass(frozen=True)
class Theme:
    """Palette used by the clock face and the alarm panel."""

    background: str = "#0a0f1f"
    glow: str = "#1b2a5c"

    bezel_outer: str = "#161d3d"
    bezel_inner: str = "#8d9bd6"
    face_edge: str = "#d5dbf5"
    face_center: str = "#fbfcff"

    tick_major: str = "#1b2559"
    tick_minor: str = "#7f88b8"
    numeral: str = "#1b2559"
    caption: str = "#8a92bf"

    hour_hand: str = "#1b2559"
    minute_hand: str = "#8e2f9f"
    second_hand: str = "#ff4b3e"
    hand_shadow: str = "#b9c0e0"

    accent: str = "#ff7a2f"
    ringing: str = "#ff3d5a"

    panel_background: str = "#10173a"
    panel_surface: str = "#1a2350"
    panel_text: str = "#eef1ff"
    panel_muted: str = "#8a92bf"
