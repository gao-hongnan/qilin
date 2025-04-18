from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, Self, overload

from rich.repr import Result

from .base import AbstractStack, T


class ArrayStack(AbstractStack[T]):
    """Stack with underlying data structure being a list. Note in our case the
    top of the stack is the end of the list. So if you push 1, 2, 3, the stack
    will be [1, 2, 3] where 3 is the top of the stack.
    """

    __slots__ = ("_values",)

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[T]) -> None: ...

    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        self._values: list[T] = []

        # NOTE: If during initialization, the user provides an iterable, we would then first instantiate the empty stack
        # by pushing each value onto the stack.
        if iterable is not None:  # NOTE: we allow empty iterable
            """NOTE: copy first to avoid mutating caller's iterable if it's a list, which it is.
            This allows us avoid any surprises and at the cost of 1 extra list allocation which we incur in Cpython's
            list.extend anyways.
            """
            buffered = list(iterable)
            self._values.extend(buffered)
            """NOTE: Why not just loop over iterable and push value?
            1. One C-level call copies the iterable into the underlying list.
            2. If future subclass overrides this class and push method change? We control what happens in this init.
            """

    @property
    def size(self) -> int:
        return self.__len__()

    def push(self, value: T) -> None:
        """
        Add a value to the top of the stack.

        Parameters
        ----------
        value : T
            The value to add to the stack.

        Time Complexity
        --------------
        O(1) amortized - occasional resizing may occur at O(n)
        """
        self._values.append(value)

    def pop(self) -> T:
        """
        Remove and return the value at the top of the stack.

        Returns
        -------
        T
            The value at the top of the stack.

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
        return self._values.pop()

    def peek(self) -> T:
        """
        Return the value at the top of the stack without removing it.

        Returns
        -------
        T
            The value at the top of the stack.

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
        return self._values[-1]

    def clear(self) -> None:
        self._values[:] = []  # NOTE: 1 C-level ops, even tho O(n) but few python instructions

    def __iter__(self) -> Iterator[T]:
        """
        Iterate through the stack from top to bottom.

        Yields
        ------
        T
            Each value in the stack, starting from the top.

        Time Complexity
        --------------
        O(n) where n is the number of values in the stack.
        """
        # NOTE: can just be return reversed(self._values), memory cheap view in CPython.
        for index in range(len(self._values) - 1, -1, -1):
            yield self._values[index]

    def __len__(self) -> int:
        return self._values.__len__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ArrayStack):
            return NotImplemented
        return self._values == other._values

    __hash__: Callable[[Self], int] | None = None  # stacks are mutable so they are not hashable

    def __str__(self) -> str:
        """
        Returns the string representation showing internal (bottom-to-top) order. So in your mind if you see
        [1, 2, 3] you should think of it as 3 plates, top plate is 3, bottom plate is 1.
        """
        if self.is_empty():
            return f"{self.__class__.__name__}([])"

        values_str = ", ".join(str(value) for value in self._values)
        return f"{self.__class__.__name__}([{values_str}])"

    def __repr__(self) -> str:
        return self.__str__()

    def __rich_repr__(self) -> Result:
        yield "values", self._values
