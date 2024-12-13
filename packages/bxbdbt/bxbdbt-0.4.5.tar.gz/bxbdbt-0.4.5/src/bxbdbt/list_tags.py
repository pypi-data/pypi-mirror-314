#!/usr/bin/env python

import logging

import click

from typing import Optional

from bxbdbt.utils import (
    get_all_tags,
    get_youngest_tag,
)


# load .env file
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)


@click.command()
@click.argument("registry_url", required=False)
@click.help_option("--help", "-h")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--youngest-tag-only",
    is_flag=True,
    help="Return only the youngest tag",
)
def main(
    registry_url: Optional[str],
    debug: bool,
    youngest_tag_only: bool,
):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s",
    )

    if not registry_url:
        raise click.ClickException(
            "Registry URL must be provided if no Containerfile is specified"
        )

    if youngest_tag_only:
        tags = get_youngest_tag(registry_url)
    else:
        tags = get_all_tags(registry_url)

    logger.debug(f"Found {len(tags)} tags")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
