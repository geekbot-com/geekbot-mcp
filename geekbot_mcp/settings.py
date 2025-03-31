import os
from pathlib import Path

import tomli


class Settings:
    server_name: str
    server_version: str
    gb_api_key: str

    def __init__(self):
        self.gb_api_key = load_api_key()
        self.server_name, self.server_version = load_package_info()


def load_api_key() -> str:
    gb_api_key = os.environ.get("GB_API_KEY")
    if not gb_api_key:
        raise ValueError(
            "GB_API_KEY is not set, please add it to your claude config file"
        )
    return gb_api_key


def load_package_info() -> tuple[str, str]:
    """Load package name and version from pyproject.toml file."""
    try:
        # Find pyproject.toml in parent directories
        current_dir = Path(__file__).parent
        project_root = current_dir

        for _ in range(3):
            if (project_root / "pyproject.toml").exists():
                break
            project_root = project_root.parent

        pyproject_path = project_root / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            pyproject_data = tomli.load(f)

        package_name = pyproject_data["project"]["name"]
        version = pyproject_data["project"]["version"]

        return package_name, version

    except (FileNotFoundError, KeyError) as e:
        raise ValueError("Failed to load package info from pyproject.toml") from e
