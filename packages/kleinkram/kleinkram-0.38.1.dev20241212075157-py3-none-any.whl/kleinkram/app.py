from __future__ import annotations

import logging
import sys
import time
from enum import Enum
from pathlib import Path
from typing import List
from typing import Optional

import typer
from click import Context
from kleinkram._version import __version__
from kleinkram.api.client import AuthenticatedClient
from kleinkram.api.routes import _claim_admin
from kleinkram.api.routes import _get_api_version
from kleinkram.auth import login_flow
from kleinkram.commands.download import download_typer
from kleinkram.commands.endpoint import endpoint_typer
from kleinkram.commands.list import list_typer
from kleinkram.commands.mission import mission_typer
from kleinkram.commands.project import project_typer
from kleinkram.commands.upload import upload_typer
from kleinkram.commands.verify import verify_typer
from kleinkram.config import Config
from kleinkram.config import get_shared_state
from kleinkram.errors import ErrorHandledTyper
from kleinkram.errors import InvalidCLIVersion
from kleinkram.utils import format_traceback
from kleinkram.utils import get_supported_api_version
from rich.console import Console
from typer.core import TyperGroup

LOG_DIR = Path() / "logs"
LOG_FILE = LOG_DIR / f"{time.time_ns()}.log"
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

# setup default logging
logger = logging.getLogger(__name__)


CLI_HELP = """\
Kleinkram CLI

The Kleinkram CLI is a command line interface for Kleinkram.
For a list of available commands, run `klein --help` or visit \
https://docs.datasets.leggedrobotics.com/usage/cli/cli-getting-started.html \
for more information.
"""


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CommandTypes(str, Enum):
    AUTH = "Authentication Commands"
    CORE = "Core Commands"
    CRUD = "Create Update Delete Commands"


class OrderCommands(TyperGroup):
    def list_commands(self, ctx: Context) -> List[str]:
        _ = ctx  # suppress unused variable warning
        return list(self.commands)


app = ErrorHandledTyper(
    cls=OrderCommands,
    help=CLI_HELP,
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
)

app.add_typer(download_typer, name="download", rich_help_panel=CommandTypes.CORE)
app.add_typer(upload_typer, name="upload", rich_help_panel=CommandTypes.CORE)
app.add_typer(verify_typer, name="verify", rich_help_panel=CommandTypes.CORE)
app.add_typer(list_typer, name="list", rich_help_panel=CommandTypes.CORE)
app.add_typer(endpoint_typer, name="endpoint", rich_help_panel=CommandTypes.AUTH)
app.add_typer(mission_typer, name="mission", rich_help_panel=CommandTypes.CRUD)
app.add_typer(project_typer, name="project", rich_help_panel=CommandTypes.CRUD)


# attach error handler to app
@app.error_handler(Exception)
def base_handler(exc: Exception) -> int:
    if not get_shared_state().debug:
        Console(file=sys.stderr).print(f"{type(exc).__name__}: {exc}", style="red")
        logger.error(format_traceback(exc))
        return 1
    raise exc


@app.command(rich_help_panel=CommandTypes.AUTH)
def login(
    key: Optional[str] = typer.Option(None, help="CLI key"),
    headless: bool = typer.Option(False),
) -> None:
    login_flow(key=key, headless=headless)


@app.command(rich_help_panel=CommandTypes.AUTH)
def logout(all: bool = typer.Option(False, help="logout on all enpoints")) -> None:
    config = Config()
    config.clear_credentials(all=all)


@app.command(hidden=True)
def claim():
    client = AuthenticatedClient()
    _claim_admin(client)
    print("admin rights claimed successfully.")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


def check_version_compatiblity() -> None:
    cli_version = get_supported_api_version()
    api_version = _get_api_version()
    api_vers_str = ".".join(map(str, api_version))

    if cli_version[0] != api_version[0]:
        raise InvalidCLIVersion(
            f"CLI version {__version__} is not compatible with API version {api_vers_str}"
        )

    if cli_version[1] != api_version[1]:
        msg = f"CLI version {__version__} might not be compatible with API version {api_vers_str}"
        Console(file=sys.stderr).print(msg, style="red")
        logger.warning(msg)


@app.callback()
def cli(
    verbose: bool = typer.Option(True, help="Enable verbose mode."),
    debug: bool = typer.Option(False, help="Enable debug mode."),
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=_version_callback
    ),
    log_level: Optional[LogLevel] = typer.Option(None, help="Set log level."),
):
    _ = version  # suppress unused variable warning
    shared_state = get_shared_state()
    shared_state.verbose = verbose
    shared_state.debug = debug

    if shared_state.debug:
        log_level = LogLevel.DEBUG

    if log_level is not None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        level = logging.getLevelName(log_level)
        logging.basicConfig(level=level, filename=LOG_FILE, format=LOG_FORMAT)
    else:
        logging.disable(logging.CRITICAL)

    logger.info(f"CLI version: {__version__}")

    try:
        check_version_compatiblity()
    except InvalidCLIVersion as e:
        logger.error(format_traceback(e))
        raise
    except Exception:
        err = ("failed to check version compatibility",)
        Console(file=sys.stderr).print(
            err, style="yellow" if shared_state.verbose else None
        )
        logger.error(err)
