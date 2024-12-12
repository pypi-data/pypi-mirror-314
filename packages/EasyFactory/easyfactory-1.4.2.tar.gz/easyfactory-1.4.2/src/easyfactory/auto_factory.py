import typing
from logging import getLogger

import factory
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

from easyfactory.pydantic import PydanticFactoryGenerator
from easyfactory.sqlalchemy import SQLAlchemyFactoryGenerator

logger = getLogger(__name__)

PT = typing.TypeVar("PT", bound=type(BaseModel))
ST = typing.TypeVar("ST", bound=type(DeclarativeBase))


def make_factory_for(model: PT | ST, **attributes: typing.Any) -> factory.Factory:
    if isinstance(model, type(BaseModel)):
        return PydanticFactoryGenerator.make_factory_for(model, **attributes)
    elif isinstance(model, type(DeclarativeBase)):
        return SQLAlchemyFactoryGenerator.make_factory_for(model, **attributes)
    raise TypeError(model)


class AutoFactoryMeta(type):
    def __new__[T](cls, name, bases, attributes: dict[str, type[T] | typing.Any]) -> T:
        x = super().__new__(cls, name, bases, attributes)
        if name == "AutoFactory":
            return x
        if (meta := attributes.get("Meta", None)) is not None:
            if (model := getattr(meta, "model", None)) is not None:
                logger.debug("model found generating Factory for `%s`", model)
                return make_factory_for(model, **attributes)
            else:
                logger.warning("Meta class found but no model inside it")
        raise TypeError(name)


class AutoFactory(metaclass=AutoFactoryMeta):
    ...
