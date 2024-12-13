from pydantic.generics import GenericModel
from typing import List
import typing as t

T = t.TypeVar('T')

class ListResponse(GenericModel, t.Generic[T]):
    total: int
    rows: List[T]