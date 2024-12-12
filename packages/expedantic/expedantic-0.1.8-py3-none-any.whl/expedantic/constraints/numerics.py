import inspect
from typing import Annotated, Generic, TypeVar
from pydantic import Field


T = TypeVar(
    "T",
)
U = TypeVar("U")

# class Range(Generic[T], Annotated[T, Field()]):


# def range(tp: type[T], **kwargs):
#     # TP = TypeVar("TP", bound=T)

#     # class Range(Annotated[type[U], Field(**kwargs)], Generic[U]): ...

#     return Range[T]

AT = Annotated[T, Field()]

A = Annotated[str, Field(min_length=3)]

RangedT = Annotated[T, Field()]


# def ranged(tp: type):
#     return Annotated[tp, Field()]


# class MyAnnot(Annotated[T, Field()]): ...


# R = Ranged[int]


def range(tp: type[T]):
    return Annotated[T, Field()]


if __name__ == "__main__":
    # r = ranged(int)
    a: MyAnnot[int] = 0
    # a: RangedT[int] = 1
