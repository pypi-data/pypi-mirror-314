from __future__ import annotations

from collections.abc import Iterable
from functools import partial
from inspect import getmembers, signature

from gdsfactory.config import logger
from gdsfactory.typings import Component, ComponentFactory


def get_cells(modules, verbose: bool = False) -> dict[str, ComponentFactory]:
    """Returns PCells (component functions) from a module or list of modules.

    Args:
        modules: module or iterable of modules.
        verbose: prints in case any errors occur.

    """
    modules = modules if isinstance(modules, Iterable) else [modules]

    cells = {}
    for module in modules:
        for t in getmembers(module):
            if callable(t[1]) and t[0] != "partial" and not t[0].startswith("_"):
                try:
                    r = signature(
                        t[1] if not isinstance(t[1], partial) else t[1].func
                    ).return_annotation
                    if r == Component or (
                        isinstance(r, str) and r.endswith("Component")
                    ):
                        cells[t[0]] = t[1]
                except ValueError as e:
                    if verbose:
                        logger.warn(f"error in {t[0]}: {e}")
    return cells


if __name__ == "__main__":
    import cspdk

    f = get_cells(cspdk.cells)
    print(f.keys())
