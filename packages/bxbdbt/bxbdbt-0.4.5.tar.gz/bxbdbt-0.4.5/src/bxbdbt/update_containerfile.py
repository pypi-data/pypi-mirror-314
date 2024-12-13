#!/usr/bin/env python

import logging

import click

from typing import Optional

# load .env file
from dotenv import load_dotenv

from bxbdbt.utils import (
    get_image_date,
    get_registry_url_from_containerfile,
    get_youngest_tag,
    update_containerfile_from,
)

load_dotenv()

logger = logging.getLogger(__name__)


@click.command()
@click.argument("registry_url", required=False)
@click.option(
    "--with-date", is_flag=True, help="Show the creation date of the latest tag"
)
@click.option(
    "--containerfile",
    type=click.Path(exists=True),
    help="Path to Containerfile to update",
)
@click.help_option("--help", "-h")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what changes would be made without actually making them",
)
def main(
    registry_url: Optional[str],
    with_date: bool,
    debug: bool,
    containerfile: Optional[str],
    dry_run: bool,
):
    """
    Get the latest tag from a container registry and optionally update a Containerfile.

    REGISTRY_URL should be in the format: registry.example.com/namespace/repository
    If --containerfile is specified and REGISTRY_URL is not provided, the registry URL
    will be extracted from the FROM line in the Containerfile.

    Authentication can be configured using REGISTRY_USERNAME and REGISTRY_PASSWORD environment variables.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s",
    )

    # If containerfile is specified but no registry_url, get it from the containerfile
    if containerfile and not registry_url:
        registry_url = get_registry_url_from_containerfile(containerfile)
        if not registry_url:
            raise click.ClickException(
                "Could not extract registry URL from Containerfile"
            )
    elif not registry_url:
        raise click.ClickException(
            "Registry URL must be provided if no Containerfile is specified"
        )

    latest_tag = get_youngest_tag(registry_url)

    if latest_tag:
        if with_date:
            date = get_image_date(registry_url, latest_tag)
            if date:
                click.echo(f"{latest_tag} ({date.strftime('%Y-%m-%d %H:%M:%S UTC')})")
            else:
                click.echo(f"{latest_tag} (date unknown)")
        else:
            click.echo(latest_tag)

        if containerfile:
            update_containerfile_from(
                containerfile, f"{registry_url}:{latest_tag}", dry_run
            )

    else:
        raise click.ClickException("Failed to get latest tag")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
