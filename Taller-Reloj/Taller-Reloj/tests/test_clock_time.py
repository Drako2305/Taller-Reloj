import unittest

from clock.clock_time import ClockTime


class ClockTimeTest(unittest.TestCase):
    def test_starts_at_midnight_by_default(self):
        self.assertEqual(ClockTime().as_tuple, (0, 0, 0))

    def test_tick_advances_seconds(self):
        clock = ClockTime(10, 20, 30)
        clock.tick()
        self.assertEqual(clock.as_tuple, (10, 20, 31))

    def test_seconds_carry_into_minutes(self):
        clock = ClockTime(10, 20, 59)
        clock.tick()
        self.assertEqual(clock.as_tuple, (10, 21, 0))

    def test_minutes_carry_into_hours(self):
        clock = ClockTime(10, 59, 59)
        clock.tick()
        self.assertEqual(clock.as_tuple, (11, 0, 0))

    def test_day_wraps_around_at_midnight(self):
        clock = ClockTime(23, 59, 59)
        clock.tick()
        self.assertEqual(clock.as_tuple, (0, 0, 0))

    def test_synchronize_ticks_when_one_second_ahead(self):
        clock = ClockTime(8, 59, 59)
        clock.synchronize(9, 0, 0)
        self.assertEqual(clock.as_tuple, (9, 0, 0))

    def test_synchronize_does_nothing_when_equal(self):
        clock = ClockTime(8, 15, 20)
        clock.synchronize(8, 15, 20)
        self.assertEqual(clock.as_tuple, (8, 15, 20))

    def test_synchronize_resets_after_a_large_gap(self):
        clock = ClockTime(8, 15, 20)
        clock.synchronize(17, 42, 5)
        self.assertEqual(clock.as_tuple, (17, 42, 5))

    def test_synchronize_handles_midnight_rollover(self):
        clock = ClockTime(23, 59, 59)
        clock.synchronize(0, 0, 0)
        self.assertEqual(clock.as_tuple, (0, 0, 0))

    def test_hand_angles_at_three_o_clock(self):
        angles = ClockTime(3, 0, 0).hand_angles()
        self.assertEqual((angles.hour, angles.minute, angles.second), (90, 0, 0))

    def test_hour_hand_uses_twelve_hour_dial(self):
        self.assertEqual(ClockTime(15, 0, 0).hand_angles().hour, 90)

    def test_hour_hand_moves_with_minutes(self):
        self.assertEqual(ClockTime(6, 30, 0).hand_angles().hour, 195)

    def test_second_fraction_makes_second_hand_sweep(self):
        angles = ClockTime(0, 0, 10).hand_angles(second_fraction=0.5)
        self.assertEqual(angles.second, 63)


if __name__ == "__main__":
    unittest.main()
