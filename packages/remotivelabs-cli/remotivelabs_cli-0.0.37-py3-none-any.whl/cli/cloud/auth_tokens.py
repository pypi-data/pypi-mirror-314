import typer

from cli.settings import settings

from .rest_helper import RestHelper as Rest

app = typer.Typer()


# TODO: add add interactive flag to set target directory # pylint: disable=fixme
@app.command(name="create", help="Create and download a new personal access token")
def create(activate: bool = typer.Option(False, help="Activate the token for use after download")) -> None:  # pylint: disable=W0621
    response = Rest.handle_post(url="/api/me/keys", return_response=True)
    pat = settings.add_personal_token(response.text)
    print(f"Personal access token added: {pat.name}")

    if not activate:
        print(f"Use 'remotive cloud auth tokens activate {pat.name}' to use this access token from cli")
    else:
        settings.activate_token(pat.name)
        print("Token file activated and ready for use")
    print("\033[93m This file contains secrets and must be kept safe")


@app.command(name="list", help="List personal access tokens")
def list_tokens() -> None:
    Rest.handle_get("/api/me/keys")


@app.command(name="revoke", help="Revoke personal access token")
def revoke(name: str = typer.Argument(help="Access token name")) -> None:
    Rest.handle_delete(f"/api/me/keys/{name}")
