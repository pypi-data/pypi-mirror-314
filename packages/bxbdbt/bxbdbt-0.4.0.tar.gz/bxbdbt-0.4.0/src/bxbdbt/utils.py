#!/usr/bin/env python

import os
import logging
import base64
import datetime
import json

from typing import List, Optional, Dict
from datetime import datetime
from urllib.parse import urlparse

import click
import requests
import requests_cache

# load .env file
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

requests_cache.install_cache("registry_cache", backend="sqlite")

DEFAULT_EXCLUDED_TAGS = [
    "latest",
    "develop",
    "master",
    "main",
    "release",
    "stable",
    "staging",
    "rawhide",
]

DEFAULT_EXCLUDED_ARCHITECTURES = ["arm64", "ppc64le", "s390x"]


def get_auth_headers(registry: str) -> Optional[Dict[str, str]]:
    """Get authentication headers using environment variables."""
    username = os.getenv("REGISTRY_USERNAME")
    password = os.getenv("REGISTRY_PASSWORD")

    if not username or not password:
        logger.debug("No authentication credentials found in environment")
        return None

    auth_string = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {
        "Authorization": f"Basic {auth_string}",
        "Accept": "application/json",
    }


def get_image_date(registry_url: str, tag: str) -> Optional[datetime]:
    """Get the creation date for a specific image tag."""
    if not registry_url.startswith(("http://", "https://")):
        registry_url = "https://" + registry_url

    parsed = urlparse(registry_url)
    registry = parsed.netloc
    repository = parsed.path.lstrip("/")

    if not registry or not repository:
        logger.error("Invalid registry URL")
        return None

    # Form the API URL for the manifest
    api_url = f"https://{registry}/v2/{repository}/manifests/{tag}"

    try:
        logger.info(f"Requesting manifest from {api_url}")
        headers = get_auth_headers(registry)
        if headers:
            headers["Accept"] = "application/vnd.docker.distribution.manifest.v2+json"

        response = requests.get(api_url, headers=headers)
        if response.status_code == 401 and headers:
            logger.warning("Authentication failed, trying anonymous access")
            response = requests.get(api_url)
        response.raise_for_status()

        manifest = response.json()
        logger.debug(f"Received manifest: {manifest}")

        if "created" in manifest:
            logger.debug(f"Found creation date in manifest: {manifest['created']}")

        # Try to get config blob if created not in manifest
        if "config" in manifest:
            logger.debug("Creation date not found in manifest, checking config blob")
            config_url = f"https://{registry}/v2/{repository}/blobs/{manifest['config']['digest']}"
            config_response = requests.get(config_url, headers=headers)
            config_response.raise_for_status()
            config = config_response.json()
            logger.debug(f"Received config: {config}")

            if "created" in config:
                logger.debug(f"Found creation date in config: {config['created']}")
                # parse config["created"] to datetime
                _created = datetime.fromisoformat(
                    config["created"].replace("Z", "+00:00")
                )

                return _created

        logger.warning("Could not find creation date in image metadata")
        return None

    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.error(f"Error getting image date: {e}")
        return None


def api_uri_from_registry(registry_url: str) -> str:
    """
    Validate the registry url and construct a API URL for the registry.

    Args:
        registry_url: URL of the container image registry
        repository: Name of the repository

    Returns:
        API URL for the registry
    """
    # Parse the URL, adding https:// if no protocol specified
    if not registry_url.startswith(("http://", "https://")):
        registry_url = "https://" + registry_url

    parsed = urlparse(registry_url)
    registry = parsed.netloc
    repository = parsed.path.lstrip("/")

    if not registry or not repository:
        logger.error("Invalid registry URL")
        raise ValueError("Invalid registry URL")

    # Form the API URL for the registry
    return f"https://{registry}/v2/{repository}/tags/list"


def filter_tags(tags: List[str], exclude_tags: List[str]) -> List[str]:
    """
    Filter out unwanted tags from a list of tags.

    Args:
        tags: List of tags to filter
        exclude_tags: List of tags to exclude

    Returns:
        Filtered list of tags
    """
    return [tag for tag in tags if tag not in exclude_tags]


def get_all_tags(registry_url: str) -> Optional[List[str]]:
    """
    Get all tags for a container image from a registry.

    Args:
        registry_url: URL of the container image registry

    Returns:
        List of all tags for the container image
    """
    api_url = api_uri_from_registry(registry_url)

    try:
        logger.debug(f"Requesting tags from {api_url}")

        # Get authentication headers
        headers = get_auth_headers(registry_url)

        # Make the API request with optional authentication
        response = requests.get(api_url, headers=headers)

        # If we get a 401, try anonymous access
        if response.status_code == 401 and headers:
            logger.warning("Authentication failed, trying anonymous access")
            response = requests.get(api_url)

        response.raise_for_status()

        # Parse the response
        data = response.json()
        logger.debug(f"Response: {data}")
        tags = data.get("tags", [])

        if not tags:
            logger.warning("No tags found in repository")
            return None

        return tags

    except requests.exceptions.RequestException as e:
        logger.error(f"Error accessing registry: {e}")
        return None


def get_architecture(registry_url: str, repository: str, tag: str) -> str:
    """
    Get the architecture of a specific image tag.

    Args:
        registry: URL of the container image registry
        repository: Name of the repository
        tag: Tag of the image

    Returns:
        The architecture of the image
    """
    headers = get_auth_headers(registry_url)
    # Get manifest first
    manifest_url = f"https://{registry_url}/v2/{repository}/manifests/{tag}"
    try:
        manifest_response = requests.get(manifest_url, headers=headers)
        if manifest_response.status_code == 401 and headers:
            manifest_response = requests.get(manifest_url)
        manifest_response.raise_for_status()
        manifest = manifest_response.json()

        logger.debug(f"Manifest for tag {tag}: {manifest}")

        if manifest.get("schemaVersion") == 1:
            data = manifest["history"][0].get("v1Compatibility")
            if data:
                v1compat_history = json.loads(data)
                return v1compat_history.get("architecture")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Manifest not found for tag: {tag}")
            return None


def get_createdAt(registry_url: str, repository: str, tag: str) -> Optional[datetime]:
    """
    Get the manifest config for a specific image tag.

    Args:
        registry: URL of the container image registry
        repository: Name of the repository
        tag: Tag of the image

    Returns:
        FIXME
    """

    headers = get_auth_headers(registry_url)
    # Get manifest first
    manifest_url = f"https://{registry_url}/v2/{repository}/manifests/{tag}"
    try:
        manifest_response = requests.get(manifest_url, headers=headers)
        if manifest_response.status_code == 401 and headers:
            manifest_response = requests.get(manifest_url)
        manifest_response.raise_for_status()
        manifest = manifest_response.json()

        logger.debug(f"Manifest for tag {tag}: {manifest}")
        if "config" in manifest:
            config_url = f"https://{registry_url}/v2/{repository}/blobs/{manifest['config']['digest']}"
            config_response = requests.get(config_url, headers=headers)
            config_response.raise_for_status()
            config = config_response.json()

            if "created" in config:
                return datetime.fromisoformat(config["created"].replace("Z", "+00:00"))
        if "history" in manifest:
            # parse the content of v1Compatibility into a dict
            data = manifest["history"][0].get("v1Compatibility")
            if data:
                v1compat_history = json.loads(data)
                if "created" in v1compat_history:
                    return datetime.fromisoformat(
                        v1compat_history.get("created").replace("Z", "+00:00")
                    )

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Manifest not found for tag: {tag}")
            return None

    return None


def get_youngest_tag(registry_url: str) -> Optional[str]:
    """
    Get the youngest (we use the creation date) tag from a container image registry.

    Args:
        registry_url: URL of the container image registry

    Returns:
        The youngest tag, or None if no tags found
    """
    # Parse the URL, adding https:// if no protocol specified
    if not registry_url.startswith(("http://", "https://")):
        registry_url = "https://" + registry_url

    parsed = urlparse(registry_url)
    registry = parsed.netloc
    repository = parsed.path.lstrip("/")

    if not registry or not repository:
        logger.debug(f"Registry: {registry}, Repository: {repository}")
        logger.error("Invalid registry URL")
        return None

    try:
        tags = get_all_tags(registry_url)

        if not tags:
            logger.warning("No tags found in repository")
            return None

        tags = filter_tags(tags, DEFAULT_EXCLUDED_TAGS)
        if not tags:
            logger.warning("No tags found after filtering")
            return None

        # Get config for all tags to find creation dates
        logger.debug(f"Tags found: {tags}")
        tag_configs = []

        for tag in tags:
            logger.debug(f"Getting config for tag: {tag}")

            if (
                get_architecture(registry, repository, tag)
                in DEFAULT_EXCLUDED_ARCHITECTURES
            ):
                logger.debug(f"Skipping tag {tag} due to excluded architecture")
                continue

            created = get_createdAt(registry, repository, tag)
            # Get config blob
            tag_configs.append((tag, created))
            logger.info(f"Tag: {tag}, Created: {created}")

        if tag_configs:
            logger.debug(f"All tags: {tag_configs}")
            # Sort by creation date and get the most recent
            latest = sorted(tag_configs, key=lambda x: x[1], reverse=True)[0][0]
            logger.info(f"Found latest tag by creation date: {latest}")
            return latest
        elif tags:
            # Fallback to last tag if no creation dates available
            latest = tags[-1]
            logger.warning(f"No creation dates available, using tag: {latest}")
            return latest

        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error accessing registry: {e}")
        return None


def update_containerfile_from(
    containerfile_path: str, new_image: str, dry_run: bool = False
) -> None:
    """
    Update the FROM line in a Containerfile with a new container image.

    Args:
        containerfile_path: Path to the Containerfile
        new_image: New container image tag to use
    """
    # Read all lines from the file
    with open(containerfile_path, "r") as f:
        lines = f.readlines()

    # Update the first line, preserving any whitespace
    if lines:
        # Find the position of 'FROM' in the first line
        first_line = lines[0]
        from_pos = first_line.find("FROM")
        if from_pos != -1:
            # Keep any leading whitespace
            lines[0] = first_line[:from_pos] + f"FROM {new_image}\n"

    if dry_run:
        click.echo(f"Would write the following content to {containerfile_path}")
        click.echo("".join(lines))
    else:
        # Write back to the file
        with open(containerfile_path, "w") as f:
            f.writelines(lines)
        logger.info(f"Updated {containerfile_path} with new image: {new_image}")


def get_registry_url_from_containerfile(containerfile_path: str) -> Optional[str]:
    """
    Extract the registry URL from the FROM line of a Containerfile.

    Args:
        containerfile_path: Path to the Containerfile

    Returns:
        The registry URL without the tag, or None if not found
    """
    try:
        with open(containerfile_path, "r") as f:
            first_line = f.readline().strip()

        if first_line.startswith("FROM "):
            image_ref = first_line[5:].strip()  # Remove "FROM " and whitespace
            # Remove tag if present
            if ":" in image_ref:
                image_ref = image_ref.split(":")[0]
            return image_ref
    except Exception as e:
        logger.error(f"Error reading Containerfile: {e}")

    return None
