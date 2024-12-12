from typing import Any, TypeVar

import factory
from faker import Faker
from pydantic import BaseModel

from easyfactory.utils import is_optional, select_generator_for_type, make_factory_class

fake = Faker()

T = TypeVar("T", bound=type(BaseModel))


def _select_generator(field_name: str, type_: type, model_fields):
    if field_name.endswith("_id") and field_name[:-3] in model_fields:
        return factory.SelfAttribute(f"{field_name[:-3]}.id")
    return select_generator_for_type(field_name, type_,
                                     lambda t: factory.SubFactory(PydanticFactoryGenerator.make_factory_for(t)))


class PydanticFactoryGenerator:
    """
    A class responsible for generating Pydantic factories dynamically based on provided attributes.
    """
    generated_factories: dict[tuple[int, str], factory.Factory | None] = {}

    @classmethod
    def make_pydantic_factory(cls, model: T, attributes: dict[str, Any]):
        """
        Generates a Pydantic factory for the given model with the specified attributes.

        :param model: The Pydantic model class for which the factory is generated.
        :type model: Type[T]
        :param attributes: Dictionary containing additional attributes to be included in the factory.
        :type attributes: dict[str, Any]
        :return: A dynamically generated Pydantic factory class.
        :rtype: factory.Factory
        """
        model_fields = model.model_fields
        attrs = {
            field: _select_generator(field, field_info.annotation, model_fields) if not is_optional(
                field_info.annotation) else None
            for field, field_info in model.model_fields.items() if field_info.is_required()
        }
        attrs.update(attributes)
        return make_factory_class(model, attrs)

    @classmethod
    def make_factory_for[T](cls, model: T, **attributes: Any) -> factory.Factory:
        """
        Generates a factory for the given Pydantic model with the specified attributes if not already existing otherwise
        return the existing one.

        :param model: The Pydantic model class for which the factory is generated.
        :type model: Type[T]
        :param attributes: Additional attributes to be included in the factory.
        :type attributes: Any
        :return: A factory class for the given Pydantic model.
        :rtype: factory.Factory
        """
        if (key := (id(model), str(attributes))) not in cls.generated_factories:
            cls.generated_factories[key] = None  # tell sub factory to not generate this value
            cls.generated_factories[key] = cls.make_pydantic_factory(model, attributes)
        return cls.generated_factories[key]
