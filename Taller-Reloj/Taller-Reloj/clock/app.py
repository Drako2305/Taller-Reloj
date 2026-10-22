"""Application controller: wires the models to the Tkinter views."""

import time
import tkinter as tk

from clock.alarm import Alarm, AlarmManager, AlarmTimeSelector
from clock.alarm_panel import AlarmPanel
from clock.clock_time import ClockTime
from clock.clock_view import AnalogClockView
from clock.theme import Theme

FRAME_INTERVAL_MS = 33
BELL_INTERVAL_SECONDS = 1.0
FLASH_INTERVAL_SECONDS = 0.4


class ClockApp:
    """Owns the window, runs the animation loop and connects alarms to the UI."""

    def __init__(self) -> None:
        self._theme = Theme()
        self._clock_time = ClockTime(*self._system_time()[:3])
        self._alarm_manager = AlarmManager()
        self._last_bell = 0.0

        self._root = tk.Tk()
        self._root.title("Analog Clock")
        self._root.configure(bg=self._theme.background)
        self._root.resizable(False, False)

        self._view = AnalogClockView(self._root, self._theme)
        self._view.pack(side="left")
        self._panel = AlarmPanel(
            self._root,
            self._theme,
            AlarmTimeSelector(),
            on_add=self._add_alarm,
            on_remove=self._remove_alarm,
            on_dismiss=self._dismiss_alarm,
        )
        self._panel.pack(side="right", fill="y")

    def run(self) -> None:
        self._update_frame()
        self._root.mainloop()

    # ---------------------------------------------------------------- alarms

    def _add_alarm(self, alarm: Alarm) -> None:
        self._alarm_manager.add(alarm)
        self._panel.show_alarms(self._alarm_manager.alarms)

    def _remove_alarm(self, alarm: Alarm) -> None:
        self._alarm_manager.remove(alarm)
        self._panel.show_alarms(self._alarm_manager.alarms)

    def _dismiss_alarm(self) -> None:
        self._alarm_manager.dismiss()
        self._panel.show_ringing(None)

    # ------------------------------------------------------------- animation

    def _update_frame(self) -> None:
        hour, minute, second, fraction, date_text = self._system_time()
        self._clock_time.synchronize(hour, minute, second)

        if self._alarm_manager.check(hour, minute) is not None:
            self._panel.show_ringing(self._alarm_manager.ringing)

        ringing = self._alarm_manager.ringing is not None
        if ringing:
            self._ring_bell()

        self._view.render(
            self._clock_time.hand_angles(fraction),
            date_text,
            self._next_alarm_text(hour, minute),
            ringing,
            flash_on=int(time.time() / FLASH_INTERVAL_SECONDS) % 2 == 0,
        )
        self._root.after(FRAME_INTERVAL_MS, self._update_frame)

    def _ring_bell(self) -> None:
        now = time.time()
        if now - self._last_bell >= BELL_INTERVAL_SECONDS:
            self._root.bell()
            self._last_bell = now

    def _next_alarm_text(self, hour: int, minute: int):
        """Text of the alarm that will ring next, or ``None`` when there are none."""
        alarms = self._alarm_manager.alarms
        if not alarms:
            return None
        upcoming = [alarm for alarm in alarms if (alarm.hour, alarm.minute) > (hour, minute)]
        return str((upcoming or alarms)[0])

    @staticmethod
    def _system_time():
        """Current local time as ``(hour, minute, second, second_fraction, date_text)``."""
        timestamp = time.time()
        local = time.localtime(timestamp)
        return (
            local.tm_hour,
            local.tm_min,
            local.tm_sec,
            timestamp % 1,
            time.strftime("%a %d %b", local).upper(),
        )
