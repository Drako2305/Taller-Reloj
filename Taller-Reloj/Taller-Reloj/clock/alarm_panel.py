"""Side panel to create, list and dismiss alarms."""

import tkinter as tk
from typing import Callable, Optional, Sequence

from clock.alarm import Alarm, AlarmTimeSelector
from clock.theme import Theme
from clock.widgets import FlatButton, arrow_button

CONTENT_PADDING = 28
BANNER_SLOT_HEIGHT = 88
LISTBOX_WIDTH = 22


class AlarmPanel(tk.Frame):
    """Lets the user pick a time with the selector rings and manage the alarm list."""

    def __init__(
        self,
        master: tk.Misc,
        theme: Theme,
        selector: AlarmTimeSelector,
        on_add: Callable[[Alarm], None],
        on_remove: Callable[[Alarm], None],
        on_dismiss: Callable[[], None],
    ) -> None:
        super().__init__(master, bg=theme.panel_background)
        self._theme = theme
        self._selector = selector
        self._on_add = on_add
        self._on_remove = on_remove
        self._on_dismiss = on_dismiss
        self._shown_alarms: Sequence[Alarm] = ()

        self._build_title()
        self._build_ringing_banner()
        self._build_time_picker()
        self._build_alarm_list()
        self._refresh_picker()

    # ---------------------------------------------------------------- build

    def _build_title(self) -> None:
        tk.Label(
            self, text="ALARMS", bg=self._theme.panel_background, fg=self._theme.accent,
            font=("Helvetica", 22, "bold"),
        ).pack(anchor="w", padx=CONTENT_PADDING, pady=(24, 0))
        tk.Label(
            self, text="Set a time and add it to your list", bg=self._theme.panel_background,
            fg=self._theme.panel_muted, font=("Helvetica", 11),
        ).pack(anchor="w", padx=CONTENT_PADDING, pady=(0, 10))

    def _build_ringing_banner(self) -> None:
        slot = tk.Frame(self, bg=self._theme.panel_background, height=BANNER_SLOT_HEIGHT)
        slot.pack(fill="x", padx=CONTENT_PADDING, pady=(0, 12))
        slot.pack_propagate(False)
        self._banner = tk.Frame(slot, bg=self._theme.ringing)
        self._banner_label = tk.Label(
            self._banner, text="", bg=self._theme.ringing, fg="#ffffff",
            font=("Helvetica", 15, "bold"),
        )
        self._banner_label.pack(pady=(10, 4))
        FlatButton(
            self._banner, text="DISMISS", command=self._on_dismiss,
            background="#ffffff", foreground=self._theme.ringing,
            font=("Helvetica", 11, "bold"), padding=(14, 3),
        ).pack(pady=(0, 10))

    def _build_time_picker(self) -> None:
        card = tk.Frame(self, bg=self._theme.panel_surface)
        card.pack(fill="x", padx=CONTENT_PADDING)

        grid = tk.Frame(card, bg=self._theme.panel_surface)
        grid.pack(pady=(10, 6))

        self._hour_label = self._build_picker_column(
            grid, 0, self._selector.next_hour, self._selector.previous_hour
        )
        tk.Label(
            grid, text=":", bg=self._theme.panel_surface, fg=self._theme.panel_muted,
            font=("Helvetica", 32, "bold"),
        ).grid(row=1, column=1, padx=6)
        self._minute_label = self._build_picker_column(
            grid, 2, self._selector.next_minute, self._selector.previous_minute
        )

        FlatButton(
            card, text="+  ADD ALARM", command=self._add_selected_alarm,
            background=self._theme.accent, foreground="#ffffff",
        ).pack(fill="x", padx=18, pady=(0, 16))

    def _build_picker_column(
        self,
        grid: tk.Frame,
        column: int,
        on_up: Callable[[], None],
        on_down: Callable[[], None],
    ) -> tk.Label:
        arrow_button(grid, self._theme, "▲", lambda: self._rotate(on_up)).grid(row=0, column=column)
        value_label = tk.Label(
            grid, text="00", bg=self._theme.panel_surface, fg=self._theme.panel_text,
            font=("Helvetica", 36, "bold"),
        )
        value_label.grid(row=1, column=column, padx=4)
        arrow_button(grid, self._theme, "▼", lambda: self._rotate(on_down)).grid(row=2, column=column)
        return value_label

    def _build_alarm_list(self) -> None:
        tk.Label(
            self, text="YOUR ALARMS", bg=self._theme.panel_background, fg=self._theme.panel_muted,
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w", padx=CONTENT_PADDING, pady=(18, 6))
        self._listbox = tk.Listbox(
            self,
            height=3,
            width=LISTBOX_WIDTH,
            bg=self._theme.panel_surface,
            fg=self._theme.panel_text,
            selectbackground=self._theme.accent,
            selectforeground="#ffffff",
            highlightthickness=0,
            borderwidth=0,
            activestyle="none",
            font=("Helvetica", 14, "bold"),
        )
        self._listbox.pack(fill="x", padx=CONTENT_PADDING)
        FlatButton(
            self, text="REMOVE SELECTED", command=self._remove_selected_alarm,
            background=self._theme.panel_surface, foreground=self._theme.panel_text,
            font=("Helvetica", 10, "bold"),
        ).pack(fill="x", padx=CONTENT_PADDING, pady=(8, 16))

    # ------------------------------------------------------------ behaviour

    def _rotate(self, rotation: Callable[[], None]) -> None:
        rotation()
        self._refresh_picker()

    def _refresh_picker(self) -> None:
        self._hour_label.configure(text=f"{self._selector.hour:02d}")
        self._minute_label.configure(text=f"{self._selector.minute:02d}")

    def _add_selected_alarm(self) -> None:
        self._on_add(self._selector.to_alarm())

    def _remove_selected_alarm(self) -> None:
        selection = self._listbox.curselection()
        if selection:
            self._on_remove(self._shown_alarms[selection[0]])

    def show_alarms(self, alarms: Sequence[Alarm]) -> None:
        """Replace the content of the alarm list."""
        self._shown_alarms = alarms
        self._listbox.delete(0, tk.END)
        for alarm in alarms:
            self._listbox.insert(tk.END, f"   {alarm}")

    def show_ringing(self, alarm: Optional[Alarm]) -> None:
        """Show the dismiss banner while ``alarm`` rings, hide it when ``None``."""
        if alarm is None:
            self._banner.pack_forget()
            return
        self._banner_label.configure(text=f"ALARM  {alarm}")
        self._banner.pack(fill="both", expand=True)
