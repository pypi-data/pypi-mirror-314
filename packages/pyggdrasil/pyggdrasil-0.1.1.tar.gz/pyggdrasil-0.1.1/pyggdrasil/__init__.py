__all__ = [
    "render_list",
    "render_tree",
]

from typing import Any, Callable, TypeVar

ELL = "└─ "
TEE = "├─ "
PIPE = "│"


def _prefix(level: int, nesting: list[bool], symbol: str) -> str:
    for index in range(level):
        if nesting[index]:
            symbol = PIPE + "  " + symbol
        else:
            symbol = "   " + symbol
    symbol = "\n" + symbol
    return symbol


Item = TypeVar("Item")


def render_list(
    lst: list[Item],
    level: int = 0,
    nesting: list[bool] | None = None,
    render: Callable[[Item], str] | None = None,
) -> str:
    if not lst:
        return ""
    render = render or (lambda _: str(_))
    nesting = nesting or [False] * level
    rendered_items = [render(item) for item in lst]
    tee = _prefix(level=level, nesting=nesting, symbol=TEE)
    ell = _prefix(level=level, nesting=nesting, symbol=ELL)
    if len(lst) == 1:
        return ell + rendered_items[0]
    return tee + (tee).join(rendered_items[:-1]) + ell + rendered_items[-1]


def render_tree(
    data: dict[Item, Any] | list[Item],
    level: int = 0,
    nesting: list[bool] | None = None,
    render: Callable[[Item], str] | None = None,
) -> str:
    nesting = nesting or [False] * level
    if isinstance(data, list):
        return render_list(data, level, nesting, render)
    if not data:
        return ""
    render = render or (lambda _: str(_))
    keys = [render(key) for key in data.keys()]
    values = list(data.values())
    tee = _prefix(level=level, nesting=nesting, symbol=TEE)
    ell = _prefix(level=level, nesting=nesting, symbol=ELL)
    result = ""

    for index, key in enumerate(keys[:-1]):
        result += tee + key
        result += render_tree(
            values[index], level=level + 1, nesting=[True] + nesting
        )

    result += ell + keys[-1]
    result += render_tree(
        values[-1], level=level + 1, nesting=[False] + nesting
    )
    return result
