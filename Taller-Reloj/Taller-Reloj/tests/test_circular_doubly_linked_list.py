import unittest

from clock.circular_doubly_linked_list import CircularDoublyLinkedList


class CircularDoublyLinkedListTest(unittest.TestCase):
    def test_empty_ring_has_no_current_value(self):
        ring = CircularDoublyLinkedList()
        self.assertTrue(ring.is_empty)
        with self.assertRaises(IndexError):
            ring.current

    def test_append_keeps_insertion_order(self):
        ring = CircularDoublyLinkedList([1, 2, 3])
        self.assertEqual(list(ring), [1, 2, 3])
        self.assertEqual(len(ring), 3)

    def test_single_node_links_to_itself(self):
        ring = CircularDoublyLinkedList(["only"])
        self.assertTrue(ring.advance())
        self.assertEqual(ring.current, "only")
        self.assertTrue(ring.rewind())
        self.assertEqual(ring.current, "only")

    def test_advance_wraps_to_head_and_reports_it(self):
        ring = CircularDoublyLinkedList([0, 1, 2])
        self.assertFalse(ring.advance())
        self.assertFalse(ring.advance())
        self.assertTrue(ring.advance())
        self.assertEqual(ring.current, 0)

    def test_rewind_wraps_to_tail_and_reports_it(self):
        ring = CircularDoublyLinkedList([0, 1, 2])
        self.assertTrue(ring.rewind())
        self.assertEqual(ring.current, 2)
        self.assertFalse(ring.rewind())
        self.assertEqual(ring.current, 1)

    def test_move_to_places_cursor_on_value(self):
        ring = CircularDoublyLinkedList(range(60))
        ring.move_to(42)
        self.assertEqual(ring.current, 42)

    def test_move_to_unknown_value_raises(self):
        ring = CircularDoublyLinkedList(range(3))
        with self.assertRaises(ValueError):
            ring.move_to(99)

    def test_reset_returns_cursor_to_head(self):
        ring = CircularDoublyLinkedList(range(5))
        ring.move_to(3)
        ring.reset()
        self.assertEqual(ring.current, 0)


if __name__ == "__main__":
    unittest.main()
