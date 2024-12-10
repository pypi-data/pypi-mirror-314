import typer

from cli.errors import ErrorPrinter
from cli.settings.core import TokenNotFoundError, settings

app = typer.Typer()


@app.command()
def describe(file: str = typer.Argument(help="Token name or file path")) -> None:
    """
    Show contents of specified access token file
    """
    try:
        print(settings.get_token_file(file))
    except TokenNotFoundError:
        ErrorPrinter.print_generic_error(f"Token file {file} not found")


@app.command()
def activate(file: str = typer.Argument(..., help="Token name or file path")) -> None:
    """
    Activate a access token file to be used for authentication.

    This will be used as the current access token in all subsequent requests. This would
    be the same as login with a browser.
    """
    try:
        settings.activate_token(file)
    except FileNotFoundError as e:
        print(f"File could not be found: {e}")


@app.command(name="list-personal-tokens")
def list_pats() -> None:
    """
    List personal access token files in remotivelabs config directory
    """
    pats = settings.list_personal_tokens()
    for pat in pats:
        print(pat.name)


@app.command(name="list-personal-tokens-files")
def list_pats_files() -> None:
    """
    List personal access token files in remotivelabs config directory
    """
    personal_files = settings.list_personal_token_files()
    for file in personal_files:
        print(file)


@app.command(name="list-service-account-tokens")
def list_sats() -> None:
    """
    List service account access token files in remotivelabs config directory
    """
    sats = settings.list_service_account_tokens()
    for sat in sats:
        print(sat.name)


@app.command(name="list-service-account-tokens-files")
def list_sats_files() -> None:
    """
    List service account access token files in remotivelabs config directory
    """
    service_account_files = settings.list_service_account_token_files()
    for file in service_account_files:
        print(file)
