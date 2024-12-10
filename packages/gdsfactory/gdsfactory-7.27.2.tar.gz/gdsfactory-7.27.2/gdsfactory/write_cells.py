"""Generate the code from a GDS file based PDK."""

from __future__ import annotations

import datetime
import pathlib
from pathlib import Path

import gdstk

from gdsfactory.component import _timestamp2019
from gdsfactory.config import PATH, logger
from gdsfactory.name import clean_name
from gdsfactory.read.import_gds import import_gds
from gdsfactory.typings import PathType

script_prefix = """
from pathlib import PosixPath
from functools import partial
import gdsfactory as gf

add_ports_optical = partial(
    gf.add_ports.add_ports_from_markers_inside, pin_layer=(1, 0), port_layer=(2, 0)
)
add_ports_electrical = partial(
    gf.add_ports.add_ports_from_markers_inside, pin_layer=(41, 0), port_layer=(1, 0)
)
add_ports = gf.compose(add_ports_optical, add_ports_electrical)

"""


def get_script(
    gdspath: PathType, module: str | None = None, add_docs: bool = False
) -> str:
    """Returns script for importing a fixed cell.

    Args:
        gdspath: fixed cell gdspath.
        module: if any includes plot directive.
        add_docs: if True adds docstring with plot directive.
    """
    cell = clean_name(gdspath.stem)
    gdspath = gdspath.stem + gdspath.suffix
    package = module.split(".")[0] if module and "." in module else module

    if add_docs:
        if module:
            return f"""

@gf.cell
def {cell}()->gf.Component:
    '''Returns {cell} fixed cell.

    .. plot::
      :include-source:

      import {package}

      c = {module}.{cell}()
      c.plot()
    '''
    return import_gds({str(gdspath)!r})

"""
        else:
            raise ValueError("module is required if add_docs is True")

    else:
        return f"""

@gf.cell
def {cell}()->gf.Component:
    '''Returns {cell} fixed cell.'''
    return import_gds({str(gdspath)!r})

"""


def get_import_gds_script(
    dirpath: PathType, module: str | None = None, add_docs: bool = False
) -> str:
    """Returns import_gds script from a directory with all the GDS files.

    Args:
        dirpath: fixed cell directory path.
        module: Optional plot directive to plot imported component.
        add_docs: if True adds docstring with plot directive.

    """
    dirpath = pathlib.Path(dirpath)
    if not dirpath.exists():
        raise ValueError(f"{str(dirpath.absolute())!r} does not exist.")

    gdspaths = (
        list(dirpath.glob("*.gds"))
        + list(dirpath.glob("*.GDS"))
        + list(dirpath.glob("*.oas"))
        + list(dirpath.glob("*.OAS"))
    )

    if not gdspaths:
        raise ValueError(f"No GDS files found at {dirpath.absolute()!r}.")

    logger.info(f"Writing {len(gdspaths)} cells from {dirpath.absolute()!r}")

    script = [script_prefix]
    script += [f"gdsdir = {str(dirpath.absolute())!r}\n"]
    script += [
        "import_gds = partial(gf.import_gds, gdsdir=gdsdir, decorator=add_ports)\n"
    ]

    cells = [
        get_script(gdspath, module=module, add_docs=add_docs) for gdspath in gdspaths
    ]
    script += sorted(cells)
    return "\n".join(script)


def write_cells_recursively(
    gdspath: PathType | None = None,
    unit: float = 1e-6,
    precision: float = 1e-9,
    timestamp: datetime.datetime | None = _timestamp2019,
    dirpath: pathlib.Path | None = None,
) -> dict[str, Path]:
    """Write gdstk cells recursively.

    Args:
        cell: gdstk cell.
        unit: unit size for objects in library. 1um by default.
        precision: for library dimensions (m). 1nm by default.
        timestamp: Defaults to 2019-10-25. If None uses current time.
        dirpath: directory for the GDS file to write to.

    Returns:
        gdspaths: dict of cell name to gdspath.
    """
    lib = gdstk.read_gds(gdspath)
    dirpath = dirpath or pathlib.Path.cwd()
    dirpath = pathlib.Path(dirpath)
    dirpath.mkdir(exist_ok=True, parents=True)
    gdspaths = {}

    for cell in lib.cells:
        gdspath = dirpath / f"{cell.name}.gds"

        lib = gdstk.Library(unit=unit, precision=precision)
        lib.add(cell)
        lib.add(*cell.dependencies(True))
        lib.write_gds(gdspath, timestamp=timestamp)
        logger.info(f"Write {cell.name!r} to {gdspath}")

        gdspaths[cell.name] = gdspath

    return gdspaths


def write_cells(
    gdspath: PathType | None = None,
    dirpath: PathType | None = None,
    unit: float = 1e-6,
    precision: float = 1e-9,
    timestamp: datetime.datetime | None = _timestamp2019,
) -> dict[str, Path]:
    """Writes cells into separate GDS files.

    Args:
        gdspath: GDS file to write cells.
        dirpath: directory path to write GDS files to.
            Defaults to current working directory.
        unit: unit size for objects in library. 1um by default.
        precision: for object dimensions in the library (m). 1nm by default.
        timestamp: Defaults to 2019-10-25. If None uses current time.

    Returns:
        gdspaths: dict of cell name to gdspath.

    """
    cell = gdstk.read_gds(gdspath)
    top_level_cells = cell.top_level()
    top_cellnames = [c.name for c in top_level_cells]

    dirpath = dirpath or pathlib.Path.cwd()
    dirpath = pathlib.Path(dirpath).absolute()
    dirpath.mkdir(exist_ok=True, parents=True)

    gdspaths = {}
    components = {}

    for cellname in top_cellnames:
        c = import_gds(gdspath=gdspath, cellname=cellname, unique_names=False)
        components[cellname] = c

    for component_name, component in components.items():
        gdspath = dirpath / f"{component_name}.gds"
        component.write_gds(
            gdspath, unit=unit, precision=precision, timestamp=timestamp
        )
        gdspaths[component_name] = gdspath
    return gdspaths


def test_write_cells_recursively() -> None:
    gdspath = PATH.gdsdir / "mzi2x2.gds"
    gdspaths = write_cells_recursively(gdspath=gdspath, dirpath="extra/gds")
    assert len(gdspaths) == 10, len(gdspaths)


def test_write_cells() -> None:
    gdspath = PATH.gdsdir / "alphabet_3top_cells.gds"
    gdspaths = write_cells(gdspath=gdspath, dirpath="extra/gds")
    assert len(gdspaths) == 3, len(gdspaths)


if __name__ == "__main__":
    # test_write_cells()
    test_write_cells_recursively()
    # gdspath = PATH.gdsdir / "alphabet_3top_cells.gds"
    # gdspaths = write_cells(gdspath=gdspath, dirpath="extra/gds", recursively=False)
    # assert len(gdspaths) == 3, len(gdspaths)

    # test_write_cells()
    # import gdsfactory as gf

    # gdspath = PATH.gdsdir / "mzi2x2.gds"
    # gdspaths = write_cells(gdspath=gdspath, dirpath="extra/gds", recursively=False)
    # assert len(gdspaths) == 10, len(gdspaths)

    # gdspath = PATH.gdsdir / "mzi2x2.gds"
    # gf.show(gdspath)
    # gdspaths = write_cells(gdspath=gdspath, dirpath="extra/gds")
    # print(len(gdspaths))

    # sample_pdk_cells = gf.grid(
    #     [
    #         gf.components.straight,
    #         gf.components.bend_euler,
    #         gf.components.grating_coupler_elliptical,
    #     ]
    # )
    # sample_pdk_cells.write_gds("extra/pdk.gds")
    # gf.write_cells.write_cells(gdspath="extra/pdk.gds", dirpath="extra/gds")
    # print(gf.write_cells.get_import_gds_script("extra/gds", module="sky130.components"))
