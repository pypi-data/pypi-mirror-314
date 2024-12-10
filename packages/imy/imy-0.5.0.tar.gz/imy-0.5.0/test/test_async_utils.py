import asyncio
import time
from typing import *  # type: ignore

import pytest

import imy.async_utils

T = TypeVar("T")


_count_concurrent_running = 0


async def _async_generator(n: int) -> AsyncIterable[int]:
    """
    Like `range`, but asynchronous.
    """
    for ii in range(n):
        yield ii


async def _count_concurrent(value: T) -> tuple[T, int]:
    """
    Returns the input value as is, as well as how often this function was
    running concurrently during the invocation. In order for this to work the
    function imposes a small delay.
    """
    global _count_concurrent_running
    _count_concurrent_running += 1

    try:
        await asyncio.sleep(0.1)
        return value, _count_concurrent_running
    finally:
        _count_concurrent_running -= 1


@pytest.mark.asyncio
async def test_collect_basic() -> None:
    result = await imy.async_utils.collect(_async_generator(5))
    assert result == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_collect_limit_too_high() -> None:
    result = await imy.async_utils.collect(_async_generator(5), limit=10)
    assert result == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_collect_limit_too_low() -> None:
    result = await imy.async_utils.collect(_async_generator(5), limit=3)
    assert result == [0, 1, 2]


@pytest.mark.asyncio
async def test_collect_empty() -> None:
    result = await imy.async_utils.collect(_async_generator(0))
    assert result == []


@pytest.mark.asyncio
async def test_amap_simple() -> None:
    results = [
        ii
        async for ii in imy.async_utils.amap(
            _count_concurrent,
            range(5),
            concurrency=100,
        )
    ]

    for ii, (value, concurrent) in enumerate(results):
        assert value == ii


@pytest.mark.asyncio
async def test_amap_concurrency() -> None:
    results = [
        ii
        async for ii in imy.async_utils.amap(
            _count_concurrent,
            range(5),
            concurrency=2,
        )
    ]

    for ii, (value, concurrent) in enumerate(results):
        assert value == ii
        assert concurrent <= 2


# TODO: Test that `amap` returns exceptions ASAP


@pytest.mark.asyncio
async def test_iterator_to_thread_simple() -> None:
    results = [
        val
        async for val in imy.async_utils.iterator_to_thread(
            range(5),
            batch_size=5,
        )
    ]

    for value_should, value_is in enumerate(results):
        assert value_should == value_is


# TODO: More tests for `iterator_to_thread`
