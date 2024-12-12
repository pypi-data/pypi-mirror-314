from __future__ import annotations

import asyncio
import inspect
import re
import time
import typing


def humanize(value=None, sep="_") -> str:
    # For future reference
    # return " ".join(
    #     "".join(y.capitalize() if i == 0 or y.isupper() else y for i, y in enumerate(x)) for x in ("get_server_UUID" or "")
    #     .split("_")
    # )
    return " ".join(x.capitalize() for x in (value or "").split(sep))


def parse_docs(docs: typing.Optional[str] = None) -> dict:
    docs = docs or ""
    directives = re.split(r"^\.\. *([^:]+):: *", docs, flags=re.MULTILINE)
    result = {"default": inspect.cleandoc(directives.pop(0)).replace("\n", " ")}

    for i in range(0, len(directives), 2):
        key = directives[i]

        params = re.split(r"^ *:([^:]+): *", directives[i + 1], flags=re.MULTILINE)
        item = {"default": inspect.cleandoc(params.pop(0)).replace("\n", " ")}

        par = {params[i]: params[i + 1] for i in range(0, len(params), 2)}
        for param_k, param_v in par.items():
            item[param_k] = inspect.cleandoc(param_v).replace("\n", " ")

        result[key] = result[key] if key in result else []
        result[key].append(item)

    return result


def to_display_name(value: str) -> str:
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", value)
    value = re.sub(r"([a-z\d])([A-Z])", r"\1 \2", value)
    value = value.replace("-", " ")
    return value


def set_interval(function: typing.Callable, delay: float = 1) -> asyncio.Task:
    """
    The set_interval() method repeatedly calls a function or executes
    a codesnippet, with a fixed time delay between each call.
    """
    delay_ns = delay * 10**9
    timer = time.perf_counter_ns()

    async def interval(timer: float):
        while True:
            response = function()
            if inspect.isawaitable(response):
                await response

            timer += delay_ns
            await asyncio.sleep((timer - time.perf_counter_ns()) / 10**9)

    return asyncio.create_task(interval(timer))


def clear_interval(interval: asyncio.Task) -> None:
    """
    The clear_interval() method cancels a timed, repeating action
    which was previously established by a call to set_interval().
    """
    interval.cancel()


__all__ = ["humanize", "parse_docs", "to_display_name", "set_interval", "clear_interval"]
