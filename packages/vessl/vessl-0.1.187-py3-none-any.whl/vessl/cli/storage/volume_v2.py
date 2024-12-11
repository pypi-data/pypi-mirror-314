from typing import Optional

import click

from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import print_table, truncate_datetime
from vessl.cli.storage import storage_cli
from vessl.storage.volume_v2 import create_volume, delete_volume, list_volumes
from vessl.util.prompt import generic_prompter, prompt_confirm


@storage_cli.command(name="volume", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_option(
    "--storage-name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
    help="The name of the storage.",
)
@vessl_option(
    "--keyword",
    type=click.STRING,
    required=False,
    default=None,
    help="Keyword to search for.",
)
@vessl_option(
    "--limit",
    type=click.INT,
    required=False,
    default=None,
)
def list(storage_name: str, keyword: Optional[str], limit: Optional[int]):
    volumes = list_volumes(storage_name=storage_name, keyword=keyword, limit=limit)
    print_table(
        volumes,
        ["Name", "Updated", "Tags"],
        lambda x: [
            x.name,
            truncate_datetime(x.updated_dt),
            [tag.name for tag in x.tags],
        ],
    )


@cli.vessl_command()
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Volume Name"),
)
@vessl_option(
    "--storage-name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
    help="The name of the storage.",
)
@vessl_option(
    "--tag",
    type=click.STRING,
    required=False,
    default=(),
    multiple=True,
    help="The tag(s) of the volume.",
)
def create(name: str, storage_name: str, tag: tuple[str, ...]):
    create_volume(name=name, storage_name=storage_name, tags=tag)


@cli.vessl_command()
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Volume Name"),
)
@vessl_option(
    "--storage-name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
    help="The name of the storage.",
)
def delete(name: str, storage_name: str):
    if not prompt_confirm(f"Are you sure to delete volume `{name}`?"):
        return

    delete_volume(name=name, storage_name=storage_name)
