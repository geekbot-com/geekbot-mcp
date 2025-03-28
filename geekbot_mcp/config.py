import os


def load_api_key():
    gb_api_key = os.environ.get("GB_API_KEY")
    if not gb_api_key:
        raise ValueError(
            "GB_API_KEY is not set, please add it to your claude config file"
        )
    return gb_api_key
