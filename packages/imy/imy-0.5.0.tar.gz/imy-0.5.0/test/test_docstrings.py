from typing import *  # type: ignore

import imy.docstrings


def _documented_function_names(docs: imy.docstrings.ClassDocs) -> set[str]:
    return {func.name for func in docs.functions}


def _documented_attribute_names(docs: imy.docstrings.ClassDocs) -> set[str]:
    return {attr.name for attr in docs.attributes}


class Parent:
    """
    # Leading Headings 1 are stripped

    This is the summary.

    This is the details. They can be very long and span multiple lines. They can
    even contain multiple paragraphs.

    Just like this one.

    ## Heading 2

    Any non-key sections are also part of the details.

    This is the end of the details.

    ## Attributes

    int_attribute: <int>

    `float_attribute`: <float>

    str_attribute: <str>

    ## Metadata

    public: False
    """

    int_attribute: int
    float_attribute: float
    str_attribute: str

    def numeric_function(self, x: int) -> float:
        """
        <function summary>

        <function details>

        ## Parameters

        x: <int>

        ## Raises

        `ValueError`: <raise-value-error>
        """
        return float(x)


class Child(Parent):
    """
    Children are parents too!

    ## Attributes

    bool_attribute: <bool>

    ## Metadata

    public: True

    experimental: True
    """

    bool_attribute: bool

    async def list_function(self, x: str) -> list:
        """
        <function summary>

        <function details>

        ## Parameters

        x: <str>
        """
        return [x]


def test_parse_class_docstring() -> None:
    docs = imy.docstrings.ClassDocs.from_class(Parent)

    assert docs.name == "Parent"
    assert docs.summary == "This is the summary."

    assert docs.details is not None
    assert docs.details.startswith("This is the details.")
    assert docs.details.endswith("This is the end of the details.")

    assert _documented_function_names(docs) == {
        "numeric_function",
    }

    for func in docs.functions:
        assert func.name == "numeric_function"
        assert func.synchronous is True
        assert func.return_type is float
        assert func.summary == "<function summary>"
        assert func.details == "<function details>"

        assert len(func.parameters) == 2
        assert func.parameters[0].name == "self"

        assert func.parameters[1].name == "x"
        assert func.parameters[1].type is int
        assert func.parameters[1].description == "<int>"

        assert len(func.raises) == 1
        assert func.raises[0] == ("ValueError", "<raise-value-error>")

    assert _documented_attribute_names(docs) == {
        "int_attribute",
        "float_attribute",
        "str_attribute",
    }

    for attr in docs.attributes:
        assert attr.type is not None
        assert attr.description is not None
        assert attr.description.strip() == f"<{attr.type.__name__}>"  # type: ignore

    assert docs.metadata.public is False
    assert docs.metadata.experimental is False


def test_parse_class_docstring_with_inheritance() -> None:
    docs = imy.docstrings.ClassDocs.from_class(Child)

    print(docs)

    assert docs.name == "Child"
    assert docs.summary == "Children are parents too!"
    assert docs.details is None

    assert _documented_function_names(docs) == {
        "numeric_function",
        "list_function",
    }

    for func in docs.functions:
        if func.name == "numeric_function":
            assert func.synchronous is True
            assert func.return_type is float
            assert func.summary == "<function summary>"
            assert func.details == "<function details>"

            assert len(func.parameters) == 2
            assert func.parameters[0].name == "self"

            assert func.parameters[1].name == "x"
            assert func.parameters[1].type is int
            assert func.parameters[1].description == "<int>"

            assert len(func.raises) == 1
            assert func.raises[0] == ("ValueError", "<raise-value-error>")

        elif func.name == "list_function":
            assert func.synchronous is False
            assert func.return_type is list
            assert func.summary == "<function summary>"
            assert func.details == "<function details>"

            assert len(func.parameters) == 2
            assert func.parameters[0].name == "self"

            assert func.parameters[1].name == "x"
            assert func.parameters[1].type is str
            assert func.parameters[1].description == "<str>"

            assert len(func.raises) == 0

        else:
            assert False, f"Unexpected function: {func.name}"

    assert _documented_attribute_names(docs) == {
        "int_attribute",
        "float_attribute",
        "str_attribute",
        "bool_attribute",
    }

    for attr in docs.attributes:
        assert attr.type is not None
        assert attr.description is not None
        assert attr.description.strip() == f"<{attr.type.__name__}>"  # type: ignore

    assert docs.metadata.public is True
    assert docs.metadata.experimental is True


test_parse_class_docstring_with_inheritance()
