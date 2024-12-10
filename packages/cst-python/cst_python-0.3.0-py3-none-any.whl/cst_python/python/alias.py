import warnings
import functools
import typing
from typing import Any, Callable, Type

class aliased:

    def __call__(self, cls:Type) -> Type:
        members = cls.__dict__.copy()

        for member_name in members:
            member = members[member_name]
            
            if hasattr(member, "_aliases"):
                for alias in member._aliases:
                    if alias in members:
                        warnings.warn(f"Class {cls.__name__} already have \
                                    member with name {alias}, alias of \
                                    {member_name} not created.")

                    setattr(cls, alias, member)

        return cls


class alias:
    def __init__(self, *aliases:str) -> None:
        self._aliases = set(aliases)

    @typing.no_type_check
    def __call__(self, method:Callable) -> Callable:
        method._aliases = self._aliases

        functools.update_wrapper(self, method)
        
        return method