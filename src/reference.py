#!/usr/bin/env python3

from __future__ import annotations
from typing import Callable, Any
import operator
from glom import glom
from enum import Enum, auto

class Op(Enum):
    UNARY = auto()
    BINARY = auto()
    REFLECTED = auto()
    FUNCTION = auto()

class Reference:
    __slots__ = ("target", "path", "history", "_initialized")

    def __init__(self, target: str, path: str | None = None, history: tuple[tuple[Callable, Any], ...] = ()):
        self.target = target
        self.path = path
        self.history = history
        
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_initialized", False):
            raise AttributeError("Reference instances are immutable after initialization")
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        if getattr(self, "_initialized", False):
            raise AttributeError("Reference instances are immutable after initialization")
        object.__delattr__(self, name)

    def _clone_with(self, **kwargs: Any) -> Reference:
        return Reference(
            target=kwargs.get("target", self.target),
            path=kwargs.get("path", self.path),
            history=kwargs.get("history", self.history)
        )

    def __getitem__(self, next_path: str) -> Reference:
        combined_path = f"{self.path}.{next_path}" if self.path else next_path
        return self._clone_with(path=combined_path)

    def resolve(self, env: dict[str, Any]) -> Any:
        if self.target in env:
            current_val = env[self.target]
        else:
            raise ValueError(f"Error: target '{self.target}' is not in env")
        if self.path:
            current_val = glom(current_val, self.path)

        for op, op_type, *rest in self.history:
            if op_type == Op.UNARY:
                current_val = op(current_val)
            elif op_type == Op.BINARY:
                other = rest[0]
                #if hasattr(other, "resolve"):
                if isinstance(other, Reference):
                    current_val = op(current_val, other.resolve(env))
                else:
                    current_val = op(current_val, other)
            elif op_type == Op.REFLECTED:
                other = rest[0]
                if hasattr(other, "resolve"):
                    current_val = op(other.resolve(env), current_val)
                else:
                    current_val = op(other, current_val)
                    
            elif op_type == Op.FUNCTION:
                args, kwargs = rest[0]
                current_val = op(current_val, *args, **kwargs)
        return current_val

    def apply(self, func: Callable, *args: Any, **kwargs: Any) -> Reference:
        history = (
            *self.history,
            (lambda current, *a, **kw: func(current, *a, **kw), Op.FUNCTION, (args, kwargs))
        )
        return self._clone_with(history=history)

    def __abs__(self) -> Reference:
        return self._clone_with(history=(*self.history, (abs, Op.UNARY)))

    def __add__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.add, Op.BINARY, other)))

    def __radd__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.add, Op.REFLECTED, other)))

    def __sub__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.sub, Op.BINARY, other)))

    def __rsub__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.sub, Op.REFLECTED, other)))

    def __mul__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.mul, Op.BINARY, other)))

    def __rmul__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.mul, Op.REFLECTED, other)))

    def __matmul__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.matmul, Op.BINARY, other)))

    def __rmatmul__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.matmul, Op.REFLECTED, other)))

    def __floordiv__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.floordiv, Op.BINARY, other)))

    def __rfloordiv__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.floordiv, Op.REFLECTED, other)))

    def __truediv__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.truediv, Op.BINARY, other)))

    def __rtruediv__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.truediv, Op.REFLECTED, other)))

    def __mod__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.mod, Op.BINARY, other)))

    def __rmod__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.mod, Op.REFLECTED, other)))

    def __pow__(self, other, mod=None) -> Reference:
        return self.apply(pow, other, mod=mod)

    def __divmod__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (divmod, Op.BINARY, other)))

    def __rdivmod__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (divmod, Op.REFLECTED, other)))

    def __lshift__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.lshift, Op.BINARY, other)))

    def __rlshift__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.lshift, Op.REFLECTED, other)))

    def __rshift__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.rshift, Op.BINARY, other)))

    def __rrshift__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.rshift, Op.REFLECTED, other)))

    def __and__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.and_, Op.BINARY, other)))

    def __rand__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.and_, Op.REFLECTED, other)))

    def __or__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.or_, Op.BINARY, other)))

    def __ror__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.or_, Op.REFLECTED, other)))

    def __xor__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.xor, Op.BINARY, other)))

    def __rxor__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.xor, Op.REFLECTED, other)))

    def __rfloordiv__(self, other: Any) -> Reference:
        return self._clone_with(history=(*self.history, (operator.floordiv, Op.REFLECTED, other)))

    def __neg__(self) -> Reference:
        return self._clone_with(history=(*self.history, (operator.neg, Op.UNARY)))

    def __invert__(self) -> Reference:
        return self._clone_with(history=(*self.history, (operator.invert, Op.UNARY)))

