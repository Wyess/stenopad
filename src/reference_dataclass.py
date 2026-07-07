#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Any
import operator
from glom import glom

@dataclass(frozen=True)
class Reference:
    target: str
    path: str | None = None
    history: tuple[tuple[Callable, Any], ...] = ()

    def __getitem__(self, next_path: str) -> Reference:
        combined_path = f"{self.path}.{next_path}" if self.path else next_path
        return replace(self, path=combined_path)

    def resolve(self, env: dict[str, Any]) -> Any:
        if self.target in env:
            current_val = env[self.target]
        else:
            raise ValueError(f"Error: target '{self.target}' is not in env")

        if self.path:
            current_val = glom(current_val, self.path)

        for op, other in self.history:
            if other is None:
                current_val = op(current_val)
            elif hasattr(other, "resolve"):
                current_val = op(current_val, other.resolve(env))
            else:
                current_val = op(current_val, other)
                    
        return current_val

    def apply(self, func: Callable, *args: Any, **kwargs: Any) -> Reference:
        history = (
            *self.history,
            (lambda current, *a, **kw: func(current, *a, **kw), (args, kwargs))
        )
        return replace(self, history=history)

    def __add__(self, other: Any) -> Reference:
        return replace(self, history=(*self.history, (operator.add, other)))

    def __radd__(self, other: Any) -> Reference:
        return self.__add__(other)

    def __sub__(self, other: Any) -> Reference:
        return replace(self, history=(*self.history, (operator.sub, other)))

    def __rsub__(self, other: Any) -> Reference:
        return replace(self, history=(*self.history, (operator.neg, None), (operator.add, other)))

    def __mul__(self, other: Any) -> Reference:
        return replace(self, history=(*self.history, (operator.mul, other)))

    def __rmul__(self, other: Any) -> Reference:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Reference:
        return replace(self, history=(*self.history, (operator.truediv, other)))

    def __rtruediv__(self, other: Any) -> Reference:
        return replace(self, history=(*self.history, (lambda current: other / current, None)))

    def __neg__(self) -> Reference:
        return replace(self, history=(*self.history, (operator.neg, None)))
 
