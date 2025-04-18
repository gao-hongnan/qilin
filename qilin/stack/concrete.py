from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Self, overload

from rich.repr import Result

from .base import AbstractStack, T


class ArrayStack(AbstractStack[T]):
    """Stack with underlying data structure being a list. Note in our case the
    top of the stack is the end of the list. So if you push 1, 2, 3, the stack
    will be [1, 2, 3] where 3 is the top of the stack.
    """

    __slots__ = ("_items",)

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[T]) -> None: ...

    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        self._items: list[T] = []

        # NOTE: If during initialization, the user provides an iterable, we would then first instantiate the empty stack
        # by pushing each item onto the stack.
        if iterable is not None:  # NOTE: we allow empty iterable
            """NOTE: copy first to avoid mutating caller's iterable if it's a list, which it is.
            This allows us avoid any surprises and at the cost of 1 extra list allocation which we incur in Cpython's
            list.extend anyways.
            """
            buffered = list(iterable)
            self._items.extend(buffered)
            """NOTE: Why not just loop over iterable and push item?
            1. One C-level call copies the iterable into the underlying list.
            2. If future subclass overrides this class and push method change? We control what happens in this init.
            """

    @property
    def size(self) -> int:
        return self.__len__()

    def push(self, item: T) -> None:
        """
        Add an item to the top of the stack.

        Parameters
        ----------
        item : T
            The item to add to the stack.

        Time Complexity
        --------------
        O(1) amortized - occasional resizing may occur at O(n)
        """
        self._items.append(item)

    def pop(self) -> T:
        """
        Remove and return the item at the top of the stack.

        Returns
        -------
        T
            The item at the top of the stack.

        Raises
        ------
        IndexError
            If the stack is empty.

        Time Complexity
        --------------
        O(1)
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """
        Return the item at the top of the stack without removing it.

        Returns
        -------
        T
            The item at the top of the stack.

        Raises
        ------
        IndexError
            If the stack is empty.

        Time Complexity
        ---------------
        O(1)
        """
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def clear(self) -> None:
        self._items[:] = []  # NOTE: 1 C-level ops, even tho O(n) but few python instructions

    def __iter__(self) -> Iterator[T]:
        """
        Iterate through the stack from top to bottom.

        Yields
        ------
        T
            Each item in the stack, starting from the top.

        Time Complexity
        --------------
        O(n) where n is the number of items in the stack.
        """
        # NOTE: can just be return reversed(self._items), memory cheap view in CPython.
        for index in range(len(self._items) - 1, -1, -1):
            yield self._items[index]

    def __len__(self) -> int:
        return self._items.__len__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ArrayStack):
            return NotImplemented
        return self._items == other._items

    __hash__: Callable[[Self], int] | None = None  # stacks are mutable so they are not hashable

    def __str__(self) -> str:
        """
        Returns the string representation showing internal (bottom-to-top) order. So in your mind if you see
        [1, 2, 3] you should think of it as 3 plates, top plate is 3, bottom plate is 1.
        """
        if self.is_empty():
            return f"{self.__class__.__name__}([])"

        items_str = ", ".join(str(item) for item in self._items)
        return f"{self.__class__.__name__}([{items_str}])"

    def __repr__(self) -> str:
        return self.__str__()

    def __rich_repr__(self) -> Result:
        yield "items", self._items
