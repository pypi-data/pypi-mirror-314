# bxbdbt

A Build Bot for Toolbx container images.

<p align="right">
    <img src="https://codeberg.org/goern/bxbdbt/media/branch/main/images/bxbdbt-logo.png" alt="BXBDBT Logo" width="300" height="300">
</p>

## Description

BXBDBT (Build Bot for Toolbx) is an automated tool that helps maintain and update Toolbx container images. It monitors container registries for new base images and automatically updates Containerfiles with the latest available versions.

## Installation

1. Clone the repository:

   ```bash
   git clone https://codeberg.org/goern/bxbdbt.git
   cd bxbdbt
   ```

2. Install using Poetry:

   ```bash
   poetry install
   ```

## Usage

BXBDBT can be used to:

1. Check for latest tags in a container registry:

   ```bash
   poetry run python src/update-containerfile.py registry.example.com/namespace/repository
   ```

2. Update a Containerfile with the latest base image:

   ```bash
   poetry run python src/update-containerfile.py --containerfile path/to/Containerfile
   ```

### Options

- `--with-date`: Show the creation date of the latest tag
- `--debug`: Enable debug logging
- `--containerfile`: PATH  Path to Containerfile to update
- `--dry-run`: Show what changes would be made without actually making them

### Authentication

Set the following environment variables for registry authentication:

- `REGISTRY_USERNAME`: Registry username
- `REGISTRY_PASSWORD`: Registry password

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Contact

- Author: goern
