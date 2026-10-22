"""Time model of the clock, made of three circular doubly linked lists."""

from dataclasses import dataclass
from typing import Tuple

from clock.circular_doubly_linked_list import CircularDoublyLinkedList

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
SECONDS_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR * SECONDS_PER_MINUTE

DEGREES_PER_SECOND = 360 / SECONDS_PER_MINUTE
DEGREES_PER_MINUTE = 360 / MINUTES_PER_HOUR
DEGREES_PER_HOUR = 360 / 12


@dataclass(frozen=True)
class HandAngles:
    """Angle of each hand in degrees, measured clockwise from the 12 o'clock mark."""

    hour: float
    minute: float
    second: float


class ClockTime:
    """Keeps the time with one ring per dial.

    ``tick`` moves the seconds ring one step; whenever a ring completes a lap
    it makes the next ring advance, exactly like the gears of a real clock.
    """

    def __init__(self, hour: int = 0, minute: int = 0, second: int = 0) -> None:
        self._seconds = CircularDoublyLinkedList(range(SECONDS_PER_MINUTE))
        self._minutes = CircularDoublyLinkedList(range(MINUTES_PER_HOUR))
        self._hours = CircularDoublyLinkedList(range(HOURS_PER_DAY))
        self.set_time(hour, minute, second)

    @property
    def hour(self) -> int:
        return self._hours.current

    @property
    def minute(self) -> int:
        return self._minutes.current

    @property
    def second(self) -> int:
        return self._seconds.current

    @property
    def as_tuple(self) -> Tuple[int, int, int]:
        return self.hour, self.minute, self.second

    @property
    def seconds_since_midnight(self) -> int:
        return (
            self.hour * MINUTES_PER_HOUR * SECONDS_PER_MINUTE
            + self.minute * SECONDS_PER_MINUTE
            + self.second
        )

    def set_time(self, hour: int, minute: int, second: int) -> None:
        """Place every ring on the given time."""
        self._hours.move_to(hour)
        self._minutes.move_to(minute)
        self._seconds.move_to(second)

    def tick(self) -> None:
        """Advance the clock by one second, carrying over to the minutes and hours."""
        if self._seconds.advance():
            if self._minutes.advance():
                self._hours.advance()

    def synchronize(self, hour: int, minute: int, second: int) -> None:
        """Follow a reference time (e.g. the system clock).

        When the reference is exactly one second ahead the rings tick, so the
        carry logic is the one doing the work; any other gap resets the rings.
        """
        target = (hour * MINUTES_PER_HOUR + minute) * SECONDS_PER_MINUTE + second
        gap = (target - self.seconds_since_midnight) % SECONDS_PER_DAY
        if gap == 1:
            self.tick()
        elif gap != 0:
            self.set_time(hour, minute, second)

    def hand_angles(self, second_fraction: float = 0.0) -> HandAngles:
        """Angles of the three hands.

        ``second_fraction`` (between 0 and 1) is the progress inside the current
        second and makes the second hand sweep smoothly instead of jumping.
        """
        seconds = self.second + second_fraction
        minutes = self.minute + seconds / SECONDS_PER_MINUTE
        hours = self.hour % 12 + minutes / MINUTES_PER_HOUR
        return HandAngles(
            hour=hours * DEGREES_PER_HOUR,
            minute=minutes * DEGREES_PER_MINUTE,
            second=seconds * DEGREES_PER_SECOND,
        )
