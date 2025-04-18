from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractStack(ABC, Generic[T]):
    """Stack inferface with LIFO/FILO semantics."""

    @property
    @abstractmethod
    def size(self) -> int: ...

    def is_empty(self) -> bool:
        return self.__len__() == 0

    @abstractmethod
    def push(self, value: T) -> None: ...

    @abstractmethod
    def pop(self) -> T: ...

    @abstractmethod
    def peek(self) -> T: ...

    @abstractmethod
    def __iter__(self) -> Iterator[T]: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def clear(self) -> None: ...

    def __bool__(self) -> bool:
        return not self.is_empty()
