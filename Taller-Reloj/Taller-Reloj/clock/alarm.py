"""Alarm feature: the alarm model, a ring-based time picker and a manager."""

from dataclasses import dataclass
from typing import Optional, Tuple

from clock.circular_doubly_linked_list import CircularDoublyLinkedList
from clock.clock_time import HOURS_PER_DAY, MINUTES_PER_HOUR


@dataclass(frozen=True, order=True)
class Alarm:
    """A daily alarm set on an hour and a minute."""

    hour: int
    minute: int

    def __str__(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"


class AlarmTimeSelector:
    """Picks the time of a new alarm by rotating two rings.

    Hours and minutes are independent circular doubly linked lists, so the
    user can go up or down past the limits and the values simply wrap.
    """

    def __init__(self, hour: int = 7, minute: int = 0) -> None:
        self._hours = CircularDoublyLinkedList(range(HOURS_PER_DAY))
        self._minutes = CircularDoublyLinkedList(range(MINUTES_PER_HOUR))
        self._hours.move_to(hour)
        self._minutes.move_to(minute)

    @property
    def hour(self) -> int:
        return self._hours.current

    @property
    def minute(self) -> int:
        return self._minutes.current

    def next_hour(self) -> None:
        self._hours.advance()

    def previous_hour(self) -> None:
        self._hours.rewind()

    def next_minute(self) -> None:
        self._minutes.advance()

    def previous_minute(self) -> None:
        self._minutes.rewind()

    def to_alarm(self) -> Alarm:
        return Alarm(self.hour, self.minute)


class AlarmManager:
    """Stores the alarms and decides when one must ring."""

    def __init__(self) -> None:
        self._alarms: list[Alarm] = []
        self._ringing: Optional[Alarm] = None
        self._last_fired_minute: Optional[Tuple[int, int]] = None

    @property
    def alarms(self) -> Tuple[Alarm, ...]:
        return tuple(self._alarms)

    @property
    def ringing(self) -> Optional[Alarm]:
        return self._ringing

    def add(self, alarm: Alarm) -> bool:
        """Store the alarm keeping the list sorted. Returns ``False`` for duplicates."""
        if alarm in self._alarms:
            return False
        self._alarms.append(alarm)
        self._alarms.sort()
        return True

    def remove(self, alarm: Alarm) -> None:
        if alarm in self._alarms:
            self._alarms.remove(alarm)

    def check(self, hour: int, minute: int) -> Optional[Alarm]:
        """Start ringing if an alarm matches the time. Fires once per minute."""
        current_minute = (hour, minute)
        if self._last_fired_minute not in (None, current_minute):
            self._last_fired_minute = None
        if self._ringing is not None or self._last_fired_minute == current_minute:
            return None
        alarm = Alarm(hour, minute)
        if alarm not in self._alarms:
            return None
        self._ringing = alarm
        self._last_fired_minute = current_minute
        return alarm

    def dismiss(self) -> None:
        self._ringing = None
