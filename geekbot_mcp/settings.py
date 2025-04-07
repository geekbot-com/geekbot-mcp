import importlib.metadata
import os


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
    """Load package name and version."""
    package_name = "geekbot-mcp"
    try:
        version = importlib.metadata.version(package_name)
        return package_name, version
    except importlib.metadata.PackageNotFoundError:  # Expected in development
        return package_name, "dev"
