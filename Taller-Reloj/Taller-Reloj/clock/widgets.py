"""Small reusable Tkinter widgets styled for the application."""

import tkinter as tk
from typing import Callable

from clock.theme import Theme, blend


class FlatButton(tk.Label):
    """Flat button with hover feedback.

    A ``Label`` is used instead of ``Button`` because native buttons ignore
    custom colors on some platforms.
    """

    def __init__(
        self,
        master: tk.Misc,
        text: str,
        command: Callable[[], None],
        background: str,
        foreground: str,
        font=("Helvetica", 12, "bold"),
        padding=(14, 8),
    ) -> None:
        super().__init__(
            master,
            text=text,
            bg=background,
            fg=foreground,
            font=font,
            padx=padding[0],
            pady=padding[1],
            cursor="hand2",
        )
        self._command = command
        self._background = background
        self._hover_background = blend(background, "#ffffff", 0.18)
        self.bind("<Enter>", lambda _event: self.configure(bg=self._hover_background))
        self.bind("<Leave>", lambda _event: self.configure(bg=self._background))
        self.bind("<Button-1>", lambda _event: self._command())


def arrow_button(master: tk.Misc, theme: Theme, text: str, command: Callable[[], None]) -> FlatButton:
    """Compact button used for the up/down arrows of the time picker."""
    return FlatButton(
        master,
        text=text,
        command=command,
        background=theme.panel_surface,
        foreground=theme.panel_text,
        font=("Helvetica", 11, "bold"),
        padding=(16, 3),
    )
