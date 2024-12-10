"""Gdsfactory loads configuration pydantic.

You can set environment variables.
"""

from __future__ import annotations

import importlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import traceback
import warnings
from enum import Enum, auto
from itertools import takewhile
from pathlib import Path
from pprint import pprint
from typing import TYPE_CHECKING, Any, ClassVar, Literal

import loguru
from dotenv import find_dotenv
from loguru import logger as logger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from loguru import Logger

__version__ = "7.27.2"
PathType = str | pathlib.Path

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent
home_path = pathlib.Path.home() / ".gdsfactory"
diff_path = repo_path / "gds_diff"
logpath = home_path / "log.log"

yamlpath_cwd = cwd / "config.yml"
yamlpath_default = module_path / "config.yml"
yamlpath_home = home_path / "config.yml"
dotenv_path = find_dotenv(usecwd=True)

GDSDIR_TEMP = pathlib.Path(tempfile.TemporaryDirectory().name).parent / "gdsfactory"

plugins = [
    "gplugins",
    "ray",
    "femwell",
    "devsim",
    "tidy3d",
    "meep",
    "meow",
    "lumapi",
    "sax",
]
pdks = [
    "aim",
    "amf",
    "ctpdk",
    "cspdk",
    "gf180",
    "gf45",
    "gvtt",
    "hhi",
    "imec",
    "sky130",
    "sph",
    "tj",
    "ubcpdk",
]


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFilter(BaseModel):
    """Filter certain messages by log level or regex.

    Filtered messages are not evaluated and discarded.
    """

    level: LogLevel = LogLevel.INFO
    regex: str | None = None

    def __call__(self, record: loguru.Record) -> bool:
        """Loguru needs the filter to be callable."""
        levelno = logger.level(self.level).no
        if self.regex is None:
            return record["level"].no >= levelno
        else:
            return record["level"].no >= levelno and not bool(
                re.search(self.regex, record["message"])
            )


class ErrorType(Enum):
    ERROR = auto()
    WARNING = auto()
    IGNORE = auto()


def print_version_plugins() -> None:
    """Print gdsfactory plugin versions and paths."""
    table = Table(title="Modules")
    table.add_column("Package", justify="right", style="cyan", no_wrap=True)
    table.add_column("version", style="magenta")
    table.add_column("Path", justify="right", style="green")

    table.add_row("python", sys.version, str(sys.executable))
    table.add_row("gdsfactory", __version__, str(module_path))

    for plugin in plugins:
        try:
            m = importlib.import_module(plugin)
            try:
                table.add_row(plugin, str(m.__version__), str(m.__path__))
            except AttributeError:
                table.add_row(plugin, "", "")
        except ImportError:
            table.add_row(plugin, "not installed", "")

    console = Console()
    console.print(table)


def print_version_plugins_raw() -> None:
    """Print gdsfactory plugin versions and paths."""
    print("python", sys.version)
    print("gdsfactory", __version__)

    for plugin in plugins:
        try:
            m = importlib.import_module(plugin)
            try:
                print(plugin, m.__version__)
            except AttributeError:
                print(plugin)
        except ImportError:
            print(plugin, "not installed", "")


def print_version_pdks() -> None:
    """Print gdsfactory PDK versions and paths."""
    table = Table(title="PDKs")
    table.add_column("Package", justify="right", style="cyan", no_wrap=True)
    table.add_column("version", style="magenta")
    table.add_column("Path", justify="right", style="green")

    for pdk in pdks:
        try:
            m = importlib.import_module(pdk)
            try:
                table.add_row(pdk, str(m.__version__), str(m.__path__))
            except AttributeError:
                table.add_row(pdk, "", "")
        except ImportError:
            table.add_row(pdk, "not installed", "")

    console = Console()
    console.print(table)


def get_number_of_cores() -> int:
    """Get number of cores/threads available.

    On (most) linux we can get it through the scheduling affinity. Otherwise,
    fall back to the multiprocessing cpu count.
    """
    try:
        threads = len(os.sched_getaffinity(0))
    except AttributeError:
        import multiprocessing

        threads = multiprocessing.cpu_count()
    return threads


def tracing_formatter(record: loguru.Record) -> str:
    """Traceback filtering.

    Filter out frames coming from Loguru internals.
    """
    frames = takewhile(
        lambda f: "/loguru/" not in f.filename, traceback.extract_stack()
    )
    stack = " > ".join(f"{f.filename}:{f.name}:{f.lineno}" for f in frames)
    record["extra"]["stack"] = stack

    if record["extra"].get("with_backtrace", False):
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level>"
            " | <cyan>{extra[stack]}</cyan> - <level>{message}</level>\n{exception}"
        )

    else:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}"
            "</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            " - <level>{message}</level>\n{exception}"
        )


class Settings(BaseSettings):
    """GDSFACTORY settings object.

    Attributes:
        n_threads: Number of threads to use for multiprocessing.
        display_type: Display type for components.
        last_saved_files: List of last saved files.
        max_name_length: Maximum length of component names.
        model_config: Pydantic model configuration.
        loglevel: Log level.
        pdk: PDK to use. Defaults to generic.
        difftest_ignore_cell_name_differences: Ignore cell name differences in difftest.
        difftest_ignore_sliver_differences: Ignore sliver differences in difftest.
        difftest_ignore_label_differences: Ignore label differences in difftest.
        layer_error_path: Layer error path.
        ports_offgrid: Ports offgrid error type.
        ports_not_manhattan: Ports not manhattan error type.
        allow_offgrid: Allows ports and polygons not to be snapped to grid on creation.
        bend_radius_error_type: Bend radius error type.
        on_width_missmatch: On width mismatch error type.
        on_layer_missmatch: On layer mismatch error type.
        on_type_missmatch: On type mismatch error type.
        default_show_suffix: Default show suffix.
        raise_error_on_mutation: Raise error on mutation.
        logger: Loguru logger.
        logfilter: Log filter.

    """

    n_threads: int = get_number_of_cores()
    display_type: Literal["klayout", "matplotlib", "kweb"] = "klayout"
    last_saved_files: list[PathType] = []
    max_name_length: int = 99
    pdk: str | None = None
    difftest_ignore_cell_name_differences: bool = True
    difftest_ignore_sliver_differences: bool = False
    difftest_ignore_label_differences: bool = False
    layer_error_path: tuple[int, int] = (1000, 0)
    ports_offgrid: Literal["warn", "error", "ignore"] = Field(
        default="ignore", description="Ensures ports are on grid."
    )
    ports_not_manhattan: Literal["warn", "error", "ignore"] = Field(
        default="ignore", description="Ensures ports are manhattan."
    )
    allow_offgrid: bool = True
    bend_radius_error_type: ErrorType = ErrorType.WARNING
    on_width_missmatch: Literal["warn", "error", "ignore"] = Field(
        default="error", description="When connecting ports with different width."
    )
    on_layer_missmatch: Literal["warn", "error", "ignore"] = Field(
        default="error", description="When connecting ports with different layers."
    )
    on_type_missmatch: Literal["warn", "error", "ignore"] = Field(
        default="error", description="When connecting ports with different types."
    )
    default_show_suffix: Literal[".oas", ".gds"] = ".gds"
    raise_error_on_mutation: bool = True
    logger: ClassVar[Logger] = logger
    logfilter: LogFilter = Field(default_factory=LogFilter)

    model_config = SettingsConfigDict(
        validation=True,
        arbitrary_types_allowed=True,
        env_file=dotenv_path,
        extra="ignore",
    )

    def __init__(self, **data: Any):
        """Set log filter and run pydantic."""

        super().__init__(**data)
        self.logger.remove()
        self.logger.add(sys.stdout, format=tracing_formatter, filter=self.logfilter)
        self.logger.debug("LogLevel: {}", self.logfilter.level)

        def showwarning(message, category, filename, lineno, *args, **kwargs):
            try:
                inferred_stack_depth = next(
                    i
                    for (
                        i,
                        stack,
                    ) in enumerate(reversed(traceback.extract_stack()))
                    if stack.lineno == lineno and stack.filename == filename
                )
            except StopIteration:
                # depth 2 would show the same line as warnings.warn with default stacklevel
                inferred_stack_depth = 2
            self.logger.opt(depth=inferred_stack_depth).warning(
                f"{category.__name__}: {message}"
            )

        warnings.showwarning = showwarning


class Paths:
    module = module_path
    repo = repo_path
    results_tidy3d = home / ".tidy3d"
    generic_tech = module / "generic_tech"
    klayout = generic_tech / "klayout"
    klayout_tech = klayout
    klayout_lyp = klayout_tech / "layers.lyp"
    klayout_yaml = generic_tech / "layer_views.yaml"
    schema_netlist = repo_path / "tests" / "schemas" / "netlist.json"
    netlists = module_path / "samples" / "netlists"
    gdsdir = repo_path / "tests" / "gds"
    thermal = repo_path / "tests" / "gds" / "thermal_phase_shifters.gds"
    gdslib = home / ".gdsfactory"
    modes = gdslib / "modes"
    sparameters = gdslib / "sp"
    capacitance = gdslib / "capacitance"
    interconnect = gdslib / "interconnect"
    optimiser = repo_path / "tune"
    notebooks = repo_path / "docs" / "notebooks"
    plugins = module / "plugins"
    test_data = repo / "test-data"
    gds_ref = test_data / "gds"
    gds_run = GDSDIR_TEMP / "gds_run"
    gds_diff = GDSDIR_TEMP / "gds_diff"
    cwd = cwd
    sparameters_repo = test_data / "sp"  # repo with some demo sparameters
    fonts = module / "components" / "fonts"
    font_ocr = fonts / "OCR-A.ttf"


CONF = Settings()
PATH = Paths()
sparameters_path = PATH.sparameters


def rich_output() -> None:
    """Enables rich output."""
    try:
        from rich import pretty

        pretty.install()
    except ImportError:
        print("You can install `pip install gdsfactory[full]` for better visualization")


def complex_encoder(z):
    if isinstance(z, pathlib.Path):
        return str(z)
    elif callable(z):
        return str(z.__name__)
    else:
        type_name = type(z)
        raise TypeError(f"Object {z} of type {type_name} is not serializable")


def write_config(config: Any, json_out_path: Path) -> None:
    """Write config to a JSON file."""
    with open(json_out_path, "w") as f:
        json.dump(config, f, indent=2, sort_keys=True, default=complex_encoder)


def print_config(key: str | None = None) -> None:
    """Prints a key for the config or all the keys."""
    if key:
        if CONF.get(key):
            print(CONF[key])
        else:
            print(f"{key!r} key not found in {CONF.keys()}")
    else:
        pprint(CONF)


def call_if_func(f: Any, **kwargs) -> Any:
    """Calls function if it's a function Useful to create objects from.

    functions if it's an object it just returns the object.
    """
    return f(**kwargs) if callable(f) else f


def get_git_hash():
    """Returns repository git hash."""
    try:
        with open(os.devnull, "w") as shutup:
            return (
                subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=shutup)
                .decode("utf-8")
                .strip("\n")
            )
    except subprocess.CalledProcessError:
        return "not_a_git_repo"


def enable_offgrid_ports() -> None:
    """Ignore off grid port warnings and allow ports not to be snapped on creation."""
    CONF.allow_offgrid = True
    CONF.ports_offgrid = "ignore"
    CONF.ports_not_manhattan = "ignore"


def disable_offgrid_ports(error_type: str = "warn") -> None:
    """Enable off grid port warnings and enforce ports to snap to 1nm grid."""
    CONF.allow_offgrid = False
    CONF.ports_offgrid = error_type
    CONF.ports_not_manhattan = error_type


def enable_off_grid_ports() -> None:
    warnings.warn(
        "enable_off_grid_ports is deprecated, use enable_offgrid_ports instead",
        DeprecationWarning,
    )
    enable_offgrid_ports()


def disable_off_grid_ports(error_type: str = "warn") -> None:
    warnings.warn(
        "disable_off_grid_ports is deprecated, use disable_offgrid_ports instead",
        DeprecationWarning,
    )
    disable_offgrid_ports(error_type)


def set_plot_options(
    show_ports: bool = True,
    show_subports: bool = False,
    label_aliases: bool = False,
    new_window: bool = False,
    blocking: bool = False,
    zoom_factor: float = 1.4,
) -> None:
    """Set plot options for matplotlib."""
    from gdsfactory.quickplotter import set_quickplot_options

    set_quickplot_options(
        show_ports=show_ports,
        show_subports=show_subports,
        label_aliases=label_aliases,
        new_window=new_window,
        blocking=blocking,
        zoom_factor=zoom_factor,
    )

    # print(PATH.sparameters)
    # print_config()
    # print_version()
    # print_version_raw()
    # print_version_pdks()
    # write_tech("tech.json")


if __name__ == "__main__":
    print(CONF.pdk)
    # print_version_plugins()
    # print_version_pdks()
