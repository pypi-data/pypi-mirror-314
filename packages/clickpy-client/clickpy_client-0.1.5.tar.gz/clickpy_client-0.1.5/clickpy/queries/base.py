from typing import Any, ClassVar, Generic, TypeVar

from pydantic import BaseModel

TModel = TypeVar('TModel')


class BaseClickPyQuery(BaseModel, Generic[TModel]):
    Model = TModel  # type: ignore
    QUERY: ClassVar[str]

    class Config:
        ignored_types = (TypeVar,)

    def __init_subclass__(cls, **kwargs: Any):
        cls.Model: type[TModel] = cls.__pydantic_generic_metadata__['args'][0]  # type: ignore

    def query(self) -> str:
        return self.QUERY.format(**self.__dict__)
