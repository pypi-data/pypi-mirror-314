import builtins
import datetime
import enum
import random
import types
import typing
import uuid
from typing import Any

import factory
from factory.base import FactoryMetaClass
from factory.declarations import BaseDeclaration
from faker import Faker

banned_prefix = ["_", "get_", "set_"]
banned_words = ["provider"]
fake = Faker()


def is_valid(word: str) -> bool:
    """
    Checks if a word is valid based on a set of banned prefixes and words.

    :param word: The word to be checked.
    :type word: str
    :return: True if the word is valid, False otherwise.
    :rtype: bool
    """
    return all(banned_word not in word for banned_word in banned_words) and all(
        not word.startswith(prefix) for prefix in banned_prefix)


faker_providers = [p for p in dir(fake) if is_valid(p)]


def is_optional(field):
    """
    Checks if a field is optional.

    :param field: The field to be checked.
    :type field: Any
    :return: True if the field is optional, False otherwise.
    :rtype: bool
    """
    return typing.get_origin(field) is typing.Union and \
        type(None) in typing.get_args(field)


def _get_faker_provider_based_on_name(field_name: str) -> str:
    """
    Retrieves the Faker provider name based on the field name.

    :param field_name: The name of the field.
    :type field_name: str
    :return: The Faker provider corresponding to the field name.
    :rtype: str
    """
    for provider in faker_providers:
        if field_name == provider:
            return provider
    return "word"


def select_faker_based_on_name(field_name: str) -> factory.Faker:
    """
    Selects a Faker provider based on the field name.

    :param field_name: The name of the field.
    :type field_name: str
    :return: A Faker object with the selected provider.
    :rtype: factory.Faker
    """
    return factory.Faker(_get_faker_provider_based_on_name(field_name))


def select_generator_for_type[T](
        field_name: str,
        type_: type[T],
        child_model_callback: typing.Callable[[type[T]], BaseDeclaration]
) -> BaseDeclaration | None:
    """
    Selects a suitable generator for a field based on its name, type, and a callback for child models.

    :param field_name: The name of the field.
    :type field_name: str
    :param type_: The type of the field.
    :type type_: type[T]
    :param child_model_callback: A callback function to handle child models.
    :type child_model_callback: typing.Callable[[type[T]], BaseDeclaration]
    :return: A suitable generator for the field.
    :rtype: BaseDeclaration | None
    """
    match type_:
        case builtins.bytes:
            return factory.Faker("binary")
        case builtins.str:
            return select_faker_based_on_name(field_name)
        case builtins.int:
            return factory.Faker("pyint")
        case builtins.float:
            return factory.Faker("pyfloat")
        case builtins.bool:
            return factory.Faker("pybool")
        case datetime.datetime:
            return factory.Faker("date_time")
        case uuid.UUID:
            return factory.LazyFunction(uuid.uuid4)
        case _:
            if isinstance(type_, enum.EnumType):
                return factory.LazyFunction(lambda: random.choice(list(type_)))

            args = typing.get_args(type_)
            match typing.get_origin(type_):
                case builtins.list:
                    value = select_generator_for_type(field_name, args[0], child_model_callback)
                    if value is not None:
                        return factory.List([value])
                    else:
                        return []
                case builtins.dict:
                    if args[0] is str:
                        return factory.Dict({getattr(fake, _get_faker_provider_based_on_name(field_name))():
                                                 select_generator_for_type(field_name, args[1], child_model_callback)})
                    else:
                        raise NotImplementedError
                        # TODO make the code below work
                        # return factory.LazyFunction(
                        #    lambda: {select_generator_for_type(field_name, args[0], submodel_callback).
                        #             evaluate(None, None, {"locale": None}):
                        #                 select_generator_for_type(field_name, args[1], submodel_callback).
                        #             evaluate(None, None, {"locale": None})})
                case types.UnionType:
                    if types.NoneType in args:
                        return None
                    # TODO implement generation in case of Union
                    raise TypeError(type_)
                case None:
                    return child_model_callback(type_)
                case _:
                    raise TypeError(type_)


def make_factory_class(model_: type, attributes: dict[str, Any]) -> factory.Factory:
    """
    Generates a factory class based on the provided model and attributes.

    :param model_: The model for which the factory class is generated.
    :type model_: type
    :param attributes: Additional attributes to be included in the factory.
    :type attributes: dict[str, Any]
    :return: A factory class.
    :rtype: factory.Factory
    """
    class MetaClass:
        model = model_

    attributes.update({"Meta": MetaClass})
    # a tuple is expected not a list, typing error is a lie !!!
    return FactoryMetaClass.__new__(FactoryMetaClass, model_.__name__ + "Factory", (factory.Factory,),
                                    attributes)
