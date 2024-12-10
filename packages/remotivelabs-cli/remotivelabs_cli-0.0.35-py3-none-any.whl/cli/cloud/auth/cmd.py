import sys

import typer

from cli.cloud.auth.login import login as do_login
from cli.cloud.rest_helper import RestHelper as Rest
from cli.errors import ErrorPrinter
from cli.settings import TokenNotFoundError, settings

from .. import auth_tokens

HELP = """
Manage how you authenticate with our cloud platform
"""
app = typer.Typer(help=HELP)
app.add_typer(auth_tokens.app, name="tokens", help="Manage users personal access tokens")


@app.command(name="login")
def login() -> None:
    """
    Login to the cli using browser

    This will be used as the current access token in all subsequent requests. This would
    be the same as activating a personal access key or service-account access key.
    """
    do_login()


@app.command()
def whoami() -> None:
    """
    Validates authentication and fetches your user information
    """
    try:
        Rest.handle_get("/api/whoami")
    except TokenNotFoundError as e:
        ErrorPrinter.print_hint(str(e))
        sys.exit(1)


@app.command()
def print_access_token() -> None:
    """
    Print current active token
    """
    try:
        print(settings.get_active_token())
    except TokenNotFoundError as e:
        ErrorPrinter.print_hint(str(e))
        sys.exit(1)


def print_access_token_file() -> None:
    """
    Print current active token and its metadata
    """
    try:
        print(settings.get_active_token_file())
    except TokenNotFoundError as e:
        ErrorPrinter.print_hint(str(e))
        sys.exit(1)


@app.command(help="Clear access token")
def logout() -> None:
    settings.clear_active_token()
    print("Access token removed")
