from __future__ import annotations

import types
import typing as t
from dataclasses import dataclass, field

import introspection.types
import introspection.typing

from . import parsers

__all__ = [
    "Unset",
    "UNSET",
    "Sentinel",
    "SENTINEL",
    "CommonMetadata",
    "Docstring",
    "ModuleDocs",
    "FunctionParameter",
    "FunctionDocs",
    "ClassField",
    "ClassDocs",
    "Property",
]


O = t.TypeVar("O")

Scope = t.Union["ModuleDocs", "ClassDocs"]
AnyDocs = t.Union[
    "ModuleDocs",
    "ClassDocs",
    "FunctionDocs",
    "Property",
    "ClassField",
    "FunctionParameter",
]


class Unset:
    pass


UNSET = Unset()


class Sentinel:
    pass


SENTINEL = Sentinel()


@dataclass
class CommonMetadata:
    """
    Some metadata such as whether an object is public or not is shared between
    different types of objects. This class is used to hold that metadata.
    """

    # Whether the object is meant to be used by users of the library, or if it's
    # an internal implementation detail.
    public: bool = True

    # If `True`, this object is not yet ready for public use. Its API may change
    # between even patch releases.
    experimental: bool = False

    # The version when this object was first added.
    added_in_version: str | None = None

    # Contains all `key: value` pairs that don't correspond to known fields
    extras: dict[str, str] = field(default_factory=dict)

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """
        Attempts to parse a boolean value from metadata.

        ## Raises

        `ValueError`: If the key is invalid.
        """
        # Postprocess the value
        if isinstance(value, str):
            value = value.strip()

        # Recognized strings
        if value == "True":
            return True

        if value == "False":
            return False

        # Invalid value
        raise ValueError(f"Cannot parse {value!r} as a boolean")

    @staticmethod
    def _parse_literal(
        metadata: dict[str, str],
        key_name: str,
        options: t.Set[str],
        default_value: str | None,
    ) -> str:
        """
        Attempts to parse a literal value from metadata.

        ## Raises

        `ValueError`: If the key is missing or invalid.
        """

        # Try to get the value
        try:
            raw = metadata[key_name]
        except KeyError:
            # No value provided
            if default_value is None:
                raise ValueError(f"Missing value for `{key_name}` in metadata")

            return default_value

        # Postprocess the value
        if isinstance(raw, str):
            raw = raw.strip()

        # Check if the value is valid
        if raw not in options:
            raise ValueError(f'Invalid value for `{key_name}` in metadata: "{raw}"')

        return raw

    @classmethod
    def from_dictionary(cls, metadata: dict[str, t.Any]) -> t.Self:
        """
        Parses a `CommonMetadata` object from a dictionary. This is useful for
        parsing metadata from a docstring key section.
        """

        kwargs = {}
        extras = {}

        type_hints = t.get_type_hints(cls)

        for key, value in metadata.items():
            try:
                annotation = type_hints[key]
            except KeyError:
                # Unknown field
                extras[key] = value
                continue

            try:
                if annotation is bool:
                    parsed_value = cls._parse_bool(value)
                elif annotation is str:
                    parsed_value = value
                else:
                    raise NotImplementedError(
                        f"Can't parse values of type {annotation} yet"
                    )
            except ValueError:
                raise ValueError(f"Invalid value for {key!r}: {value!r}")

            kwargs[key] = parsed_value

        # Construct the result
        return cls(**kwargs, extras=extras)


@dataclass
class FunctionMetadata(CommonMetadata):
    decorator: bool = False


@dataclass
class ClassMetadata(CommonMetadata):
    pass


@dataclass
class Docstring:
    """
    A generic docstring object.

    Docstrings are split into multiple sections: The **summary** is a brief,
    one-line description of the object. This is intended to be displayed right
    next to the object's name in a list of objects for example.

    The **details** section is a more in-depth explanation of the object. This
    may span multiple paragraphs and gives an explanation of the object

    Finally, **key_sections** are sections which consist entirely of `key:
    value` pairs. These can be used for raised exceptions, parameters, and
    similar.
    """

    summary: str | None
    details: str | None

    key_sections: dict[str, dict[str, str]]

    @staticmethod
    def from_string(
        docstring: str,
        *,
        key_sections: t.Iterable[str],
    ) -> Docstring:
        return parsers.parse_docstring(
            docstring,
            key_sections=key_sections,
        )


@dataclass
class Deprecation:
    since_version: str
    message: str | None = None
    will_be_removed_in_version: str | None = None


@dataclass
class FunctionParameter:
    owning_function: FunctionDocs

    name: str
    type: introspection.types.TypeAnnotation | Unset
    default: t.Any | Unset

    kw_only: bool

    collect_positional: bool
    collect_keyword: bool

    description: str | None

    deprecations: list[Deprecation]

    def transform_docstrings(self, transform: t.Callable[[t.Self, str], str]) -> None:
        if self.description is not None:
            self.description = transform(self, self.description)


@dataclass
class _ObjectDocs(t.Generic[O]):
    """
    Base class for everything that's an object, i.e. exists at runtime.
    (i.e. modules, classes, functions.)
    """

    object: O

    # These two attributes contain the *public* name/location of this object,
    # *not* the location where it was defined. For example, the `owning_scope`
    # of `requests.Session` would be the `requests` module, even though that
    # class is defined in the `requests.session` sub-module.
    owning_scope: Scope | None
    name: str

    summary: str | None
    details: str | None

    deprecations: list[Deprecation]

    @property
    def full_name(self) -> str:
        """
        The "full name" of this object, in other words, how users are expected
        to access it. (For example, "requests.Session")
        """
        parts = list[str]()

        obj = self
        while obj is not None:
            parts.append(obj.name)
            obj = obj.owning_scope

        parts.reverse()
        return ".".join(parts)

    def transform_docstrings(self, transform: t.Callable[[t.Self, str], str]) -> None:
        if self.summary is not None:
            self.summary = transform(self, self.summary)

        if self.details is not None:
            self.details = transform(self, self.details)


@dataclass
class ModuleDocs(_ObjectDocs[types.ModuleType]):
    """
    A docstring specifically for modules.
    """

    members: dict[str, ModuleDocs | ClassDocs | FunctionDocs] = field(repr=False)

    metadata: CommonMetadata

    @staticmethod
    def from_module(
        module: types.ModuleType,
        *,
        owning_scope: Scope | None = None,
    ) -> ModuleDocs:
        """
        Parses a `ModuleDocs` object from a module object.
        """
        return parsers.parse_module(module, owning_scope=owning_scope)

    def add_member(
        self,
        member: type | types.FunctionType | types.ModuleType,
        *,
        name: str | None = None,
    ) -> None:
        """
        Adds the given object to this module. You can use this method to add
        objects that were incorrectly assumed to be private.
        """
        docs = parsers.parse(member, owning_scope=self)

        if name is None:
            name = docs.name

        self.members[name] = docs

    def iter_children(
        self, *, include_self: bool, recursive: bool
    ) -> t.Iterable[AnyDocs]:
        if include_self:
            yield self

        for member in self.members.values():
            yield member

            if recursive:
                yield from member.iter_children(include_self=False, recursive=True)


@dataclass
class FunctionDocs(_ObjectDocs[t.Callable]):
    """
    A docstring specifically for functions and methods.
    """

    parameters: list[FunctionParameter]
    return_type: introspection.types.TypeAnnotation | Unset
    synchronous: bool
    class_method: bool
    static_method: bool

    raises: list[tuple[str, str]]  # type, description

    metadata: FunctionMetadata

    @staticmethod
    def from_function(
        func: t.Callable,
        *,
        owning_scope: Scope | None = None,
    ) -> FunctionDocs:
        """
        Parses a `FunctionDocs` object from a function or method. This takes
        both the function's docstring as well as its signature and type hints
        into account.
        """
        return parsers.parse_function(func, owning_scope=owning_scope)

    def iter_children(
        self, *, include_self: bool, recursive: bool
    ) -> t.Iterable[FunctionDocs | FunctionParameter]:
        if include_self:
            yield self

        yield from self.parameters


@dataclass
class ClassField:
    owning_class: ClassDocs

    name: str
    type: introspection.types.TypeAnnotation | Unset
    default: object | Unset

    description: str | None

    def transform_docstrings(self, transform: t.Callable[[t.Self, str], str]) -> None:
        if self.description is not None:
            self.description = transform(self, self.description)


@dataclass
class Property:
    owning_class: ClassDocs

    name: str
    getter: FunctionDocs
    setter: FunctionDocs | None

    @staticmethod
    def from_property(
        prop: property,
        owning_class: type | ClassDocs,
    ) -> Property:
        assert prop.fget is not None
        getter = FunctionDocs.from_function(prop.fget)

        if prop.fset is None:
            setter = None
        else:
            setter = FunctionDocs.from_function(prop.fset)

        if not isinstance(owning_class, ClassDocs):
            owning_class = ClassDocs.from_class(owning_class)

        return Property(
            owning_class=owning_class,
            name=getter.name,
            getter=getter,
            setter=setter,
        )

    def iter_children(
        self, *, include_self: bool, recursive: bool
    ) -> t.Iterable[Property | FunctionDocs | FunctionParameter]:
        if include_self:
            yield self

        yield self.getter
        if recursive:
            yield from self.getter.iter_children(include_self=False, recursive=True)

        if self.setter is not None:
            yield self.setter
            if recursive:
                yield from self.setter.iter_children(include_self=False, recursive=True)

    def transform_docstrings(
        self, transform: t.Callable[[t.Self | FunctionDocs, str], str]
    ) -> None:
        self.getter.transform_docstrings(transform)

        if self.setter is not None:
            self.setter.transform_docstrings(transform)


@dataclass
class ClassDocs(_ObjectDocs[type]):
    """
    A docstring specifically for classes.
    """

    attributes: list[ClassField]
    properties: list[Property]
    functions: list[FunctionDocs]

    metadata: ClassMetadata

    @staticmethod
    def from_class(
        typ: type,
        *,
        owning_scope: Scope | None = None,
    ) -> ClassDocs:
        """
        Parses a `ClassDocs` object from a class. This takes both the class's
        docstring as well as its methods and attributes into account.
        """

        return parsers.parse_class(typ, owning_scope=owning_scope)

    def iter_children(
        self, *, include_self: bool, recursive: bool
    ) -> t.Iterable[
        ClassDocs | ClassField | Property | FunctionDocs | FunctionParameter
    ]:
        if include_self:
            yield self

        yield from self.attributes

        for prop in self.properties:
            yield prop

            if recursive:
                yield from prop.iter_children(include_self=False, recursive=True)

        for function in self.functions:
            yield function

            if recursive:
                yield from function.iter_children(include_self=False, recursive=True)
