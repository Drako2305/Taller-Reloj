"""A circular doubly linked list with a movable cursor.

The list is the only data structure the clock relies on: every dial of the
clock (seconds, minutes, hours) is a ring whose cursor points at the current
value. Moving the cursor past the last element wraps back to the first one,
which is exactly the behaviour of a clock dial.
"""

from typing import Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """A single element of the ring, linked to its neighbours in both directions."""

    __slots__ = ("value", "previous", "next")

    def __init__(self, value: T) -> None:
        self.value = value
        self.previous: "Node[T]" = self
        self.next: "Node[T]" = self


class CircularDoublyLinkedList(Generic[T]):
    """Ring of values with a cursor that can move forward and backward.

    The first appended value is the *head*. The cursor starts on the head and
    ``advance`` / ``rewind`` report whether the move crossed the head, which is
    what lets a seconds ring tell the minutes ring that a full lap was made.
    """

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._head: Optional[Node[T]] = None
        self._cursor: Optional[Node[T]] = None
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        """Yield every value exactly once, starting from the head."""
        node = self._head
        for _ in range(self._size):
            assert node is not None
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return f"CircularDoublyLinkedList({list(self)!r})"

    @property
    def is_empty(self) -> bool:
        return self._size == 0

    @property
    def current(self) -> T:
        """Value under the cursor."""
        return self._require_cursor().value

    def append(self, value: T) -> None:
        """Insert ``value`` just before the head, i.e. at the end of the ring."""
        node = Node(value)
        if self._head is None:
            self._head = node
            self._cursor = node
        else:
            tail = self._head.previous
            node.previous = tail
            node.next = self._head
            tail.next = node
            self._head.previous = node
        self._size += 1

    def advance(self) -> bool:
        """Move the cursor one step forward.

        Returns ``True`` when the move wrapped around to the head.
        """
        cursor = self._require_cursor()
        self._cursor = cursor.next
        return self._cursor is self._head

    def rewind(self) -> bool:
        """Move the cursor one step backward.

        Returns ``True`` when the move wrapped around from the head to the tail.
        """
        cursor = self._require_cursor()
        wrapped = cursor is self._head
        self._cursor = cursor.previous
        return wrapped

    def move_to(self, value: T) -> None:
        """Place the cursor on the first node holding ``value``.

        Raises ``ValueError`` if the value is not in the ring.
        """
        node = self._head
        for _ in range(self._size):
            assert node is not None
            if node.value == value:
                self._cursor = node
                return
            node = node.next
        raise ValueError(f"{value!r} is not in the ring")

    def reset(self) -> None:
        """Put the cursor back on the head."""
        self._cursor = self._head

    def _require_cursor(self) -> Node[T]:
        if self._cursor is None:
            raise IndexError("the ring is empty")
        return self._cursor
