from typing import Any
from htmlmin import minify


def compress(html: str, **kwargs: Any) -> str:
    return minify(html, **kwargs)
