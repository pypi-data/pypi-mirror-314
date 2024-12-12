from typing import Any, Never, TypeVar

import factory
from factory import Factory
from sqlalchemy.orm import InstrumentedAttribute, Mapper
from sqlalchemy.orm.decl_api import DeclarativeBase

from easyfactory.utils import select_generator_for_type, make_factory_class

T = TypeVar("T", bound=type(DeclarativeBase))


def load_type[T](mappers: frozenset[Mapper], type_name: str) -> type[T]:
    """
    Load a class from sqlalchemy registry (useful for Mapped["className"])
    :param mappers: the list of mappers to search for
    :param type_name: the name of the type to load
    :return: the python type woth given name
    """
    for mapper in mappers:
        if mapper.entity.__name__ == type_name:
            return mapper.entity
    raise TypeError(type_name)


def make_post_gen(
        field_name: str,
        sub_factory_model: type[Factory],
        remote_prop_name: str,
        local_use_list: bool,
        remote_use_list: bool | None
):
    """
    generate a postgen function that will generate the relationship model and set the relation properties such
        that X.y == Y and Y.x == X or X.y==[Y] and Y.x == X or X.y == X and Y.x == [Y]
        depending on declared relation on model

    :param field_name: the local field name to populate
    :param sub_factory_model: the sub factory model to instantiate
    :param remote_prop_name: the property name on the sub object to use for linking with parent
    :param local_use_list: should we set the local property to Parent.field_name = `[Child]` or `Child`
    :param remote_use_list: should we set the remote property to Child.remote_prop_name =`[Parent]` or `Parent`
    :return: a post_gen function
    """

    def post_gen(obj, create, extracted, **kwargs):
        if extracted is not None:
            value = extracted
        else:
            if remote_use_list is None:
                additional_args = {}
            else:
                additional_args = {remote_prop_name: [obj] if remote_use_list else obj}
            value = sub_factory_model(**additional_args, **kwargs)
            if local_use_list:
                value = [value]
        setattr(obj, field_name, value)

    return post_gen


def _select_generator_for_standard_property(field_name: str, type_: type, model_fields):
    """
    get the value generator for a base python type (called for non relationship properties of a model)

    :param field_name: the name of the property
    :param type_: the type of the property to get a generator for
    :param model_fields: the list of fields for this model
        (used to override generation if a property with the same name without _id exist)
        e.g. host_id and host will make host_id get value from host instead of generating an invalid id
    :return: a generator for the type
    """
    if field_name.endswith("_id") and field_name[:-3] in model_fields:
        # not SelfAttribute or LazyAttribute because we need to be in post gen
        return factory.PostGeneration(
            lambda obj, create, extracted, **kwargs: getattr(getattr(obj, field_name[:-3]), "id", None))

    def handler(*args, **kwargs) -> Never:
        raise ValueError(*args, kwargs)  # pragma: no cover

    return select_generator_for_type(field_name, type_, handler)


def _make_post_gen_for_relationship(field_name: str,
                                    type_: type,
                                    model_fields: dict[str, Any],
                                    remote_prop_name: str | None,
                                    local_use_list: bool | None,
                                    remote_use_list: bool | None):
    if field_name.endswith("_id") and field_name[:-3] in model_fields:
        # not SelfAttribute or LazyAttribute because we need to be in post gen
        return factory.PostGeneration(
            lambda obj, create, extracted, **kwargs: getattr(getattr(obj, field_name[:-3]), "id", None))

    def handle_child_model[T](type_: type[T]):
        additional_properties = {}
        if remote_prop_name is not None:
            additional_properties[remote_prop_name] = None
        sub_factory_model = SQLAlchemyFactoryGenerator.make_factory_for(type_, **additional_properties)
        if sub_factory_model is not None:
            post_gen = make_post_gen(field_name, sub_factory_model, remote_prop_name, local_use_list, remote_use_list)
            return factory.PostGeneration(post_gen)
        else:
            return None

    return select_generator_for_type(field_name, type_, handle_child_model)


def _sqlalchemy_select_generator(mappers, attribute_name, attribute_value, attributes):
    if hasattr(attribute_value, "nullable"):  # standard prop
        if attribute_value.nullable is True:
            return None
        return _select_generator_for_standard_property(attribute_name, attribute_value.type.python_type, attributes)
    else:  # relationship
        prop = attribute_value.property
        argument = prop.argument
        if isinstance(argument, str):
            python_type = load_type(mappers, argument)
        else:
            python_type = argument
        return _make_post_gen_for_relationship(
            attribute_name,
            python_type,
            attributes,
            prop.back_populates,
            prop.uselist,
            prop.mapper.attrs[prop.back_populates].uselist if prop.back_populates is not None else None
        )


class SQLAlchemyFactoryGenerator:
    """
    A class responsible for generating SQLAlchemy factories dynamically based on provided attributes.
    """
    generated_factories: dict[tuple[int, str], factory.Factory | None] = {}

    @classmethod
    def make_sqlalchemy_factory(cls, model: T, attributes: dict[str, Any]):
        """
        Generates a SQLAlchemy factory for the given model with the specified attributes.

        :param model: The SQLAlchemy model class for which the factory is generated.
        :type model: Type[T]
        :param attributes: Dictionary containing additional attributes to be included in the factory.
        :type attributes: dict[str, Any]
        :return: A dynamically generated SQLAlchemy factory class.
        :rtype: factory.Factory
        """
        attrs = {}
        # Extracting original attributes from the model
        original_attrs = {key: value for key, value in vars(model).items() if not key.startswith("_")}

        for attr, attribute_value in original_attrs.items():
            # Skip attributes that are already present in the provided attributes
            if attr in attributes:
                continue
            if isinstance(attribute_value, InstrumentedAttribute):
                if (generator := _sqlalchemy_select_generator(model._sa_registry.mappers, attr, attribute_value,
                                                              original_attrs, )) is not None:
                    attrs[attr] = generator

        attrs.update(attributes)
        return make_factory_class(model, attrs)

    @classmethod
    def make_factory_for[T](cls, model: T, **attributes: Any) -> factory.Factory:
        """
        Generates a factory for the given model with the specified attributes if not already existing otherwise
        return the existing one.

        :param model: The SQLAlchemy model class for which the factory is generated.
        :type model: Type[T]
        :param attributes: Additional attributes to be included in the factory.
        :type attributes: Any
        :return: A factory class for the given model.
        :rtype: factory.Factory
        """
        if (key := (id(model), str(attributes))) not in cls.generated_factories:
            cls.generated_factories[key] = None  # tell sub factory to not generate this value
            cls.generated_factories[key] = cls.make_sqlalchemy_factory(model, attributes)
        return cls.generated_factories[key]
