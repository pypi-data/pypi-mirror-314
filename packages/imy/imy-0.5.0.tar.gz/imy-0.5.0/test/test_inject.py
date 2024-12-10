from typing import *  # type: ignore

import pytest

import imy.inject


class A:
    pass


class B:
    pass


class B_A(B):
    pass


class C:
    pass


class D:
    pass


class E:
    pass


def make_injector() -> imy.inject.Injector:
    """
    Creates a fresh injector without any instantiated components.
    """
    injector = imy.inject.Injector()

    @injector.bind()
    def create_a() -> A:
        return A()

    @injector.bind(B)
    def create_b_a() -> B_A:
        return B_A()

    @injector.bind()
    def create_c(a: A, b: B) -> C:
        assert isinstance(a, A)
        assert isinstance(b, B)
        return C()

    @injector.bind()
    def create_d(e: E) -> D:
        assert isinstance(e, E)
        return D()

    @injector.bind()
    def create_e(d: D) -> E:
        assert isinstance(d, D)
        return E()

    return injector


def test_get_a() -> None:
    injector = make_injector()
    a = injector[A]
    assert isinstance(a, A)


def test_get_b() -> None:
    injector = make_injector()
    b = injector[B]
    assert isinstance(b, B_A)


def test_get_c() -> None:
    injector = make_injector()
    c = injector[C]
    assert isinstance(c, C)


def test_get_d() -> None:
    injector = make_injector()

    with pytest.raises(imy.inject.DependencyCycleError):
        injector[D]


def test_inject_subtyped() -> None:
    """
    Injectors aren't supposed to distinguish by the "args" of a type, i.e.
    `list[int]` and `list[str]` are the same type to them. Verify that.
    """
    injector = imy.inject.Injector()

    @injector.bind()
    def create_list_int() -> list[int]:
        return [1, 2, 3]

    result = injector[list]
    assert result == [1, 2, 3]


def test_inject_subtyped_clash() -> None:
    """
    Make sure injectors don't allow two different subtypes of the same type.
    """
    injector = imy.inject.Injector()

    @injector.bind()
    def create_list_int() -> list[int]:
        return [1, 2, 3]

    with pytest.raises(TypeError):

        @injector.bind()
        def create_list_str() -> list[str]:
            return ["a", "b", "c"]


def test_duplicate_loggers_with_clear() -> None:
    """
    Registering duplicate factories is fine, as long as the injector is cleared
    before the second registration.
    """

    injector = imy.inject.Injector()

    @injector.bind()
    def create_a() -> A:
        return A()

    injector.clear()

    @injector.bind()
    def create_a_again() -> A:
        return A()
