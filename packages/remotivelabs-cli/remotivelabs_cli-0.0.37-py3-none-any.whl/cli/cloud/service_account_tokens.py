import json

import typer

from cli.settings import settings

from .rest_helper import RestHelper as Rest

app = typer.Typer()


# TODO: add add interactive flag to set target directory # pylint: disable=fixme
@app.command(name="create", help="Create and download a new service account access token")
def create(
    expire_in_days: int = typer.Option(default=365, help="Number of this token is valid"),
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    response = Rest.handle_post(
        url=f"/api/project/{project}/admin/accounts/{service_account}/keys",
        return_response=True,
        body=json.dumps({"daysUntilExpiry": expire_in_days}),
    )

    sat = settings.add_service_account_token(service_account, response.text)
    print(f"Service account access token added: {sat.name}")
    print("\033[93m This file contains secrets and must be kept safe")


@app.command(name="list", help="List service account access tokens")
def list_tokens(
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_get(f"/api/project/{project}/admin/accounts/{service_account}/keys")


@app.command(name="revoke", help="Revoke service account access token")
def revoke(
    name: str = typer.Argument(..., help="Access token name"),
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_delete(f"/api/project/{project}/admin/accounts/{service_account}/keys/{name}")
