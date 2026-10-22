import unittest

from clock.alarm import Alarm, AlarmManager, AlarmTimeSelector


class AlarmTimeSelectorTest(unittest.TestCase):
    def test_default_time(self):
        selector = AlarmTimeSelector()
        self.assertEqual(selector.to_alarm(), Alarm(7, 0))

    def test_hours_wrap_forward_and_backward(self):
        selector = AlarmTimeSelector(hour=23)
        selector.next_hour()
        self.assertEqual(selector.hour, 0)
        selector.previous_hour()
        self.assertEqual(selector.hour, 23)

    def test_minutes_wrap_without_touching_hours(self):
        selector = AlarmTimeSelector(hour=5, minute=59)
        selector.next_minute()
        self.assertEqual((selector.hour, selector.minute), (5, 0))
        selector.previous_minute()
        self.assertEqual((selector.hour, selector.minute), (5, 59))


class AlarmManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = AlarmManager()

    def test_alarms_are_kept_sorted_without_duplicates(self):
        self.assertTrue(self.manager.add(Alarm(9, 30)))
        self.assertTrue(self.manager.add(Alarm(6, 15)))
        self.assertFalse(self.manager.add(Alarm(6, 15)))
        self.assertEqual(self.manager.alarms, (Alarm(6, 15), Alarm(9, 30)))

    def test_remove_alarm(self):
        self.manager.add(Alarm(6, 15))
        self.manager.remove(Alarm(6, 15))
        self.assertEqual(self.manager.alarms, ())

    def test_matching_time_starts_ringing(self):
        self.manager.add(Alarm(6, 15))
        self.assertIsNone(self.manager.check(6, 14))
        self.assertEqual(self.manager.check(6, 15), Alarm(6, 15))
        self.assertEqual(self.manager.ringing, Alarm(6, 15))

    def test_alarm_does_not_ring_again_in_the_same_minute(self):
        self.manager.add(Alarm(6, 15))
        self.manager.check(6, 15)
        self.manager.dismiss()
        self.assertIsNone(self.manager.check(6, 15))
        self.assertIsNone(self.manager.ringing)

    def test_alarm_rings_again_the_next_day(self):
        self.manager.add(Alarm(6, 15))
        self.manager.check(6, 15)
        self.manager.dismiss()
        self.manager.check(6, 16)
        self.assertEqual(self.manager.check(6, 15), Alarm(6, 15))


if __name__ == "__main__":
    unittest.main()
