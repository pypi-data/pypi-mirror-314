import json
import os

CONFIG_FILE = os.path.expanduser("~/.verbia/config.json")

user_available_config_keys = ["gemini_api_key"]


def get_user_available_config() -> dict[str, str]:
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    return {key: config.get(key, "N/A") for key in user_available_config_keys}


def get_config(key: str) -> str:
    directory = os.path.dirname(CONFIG_FILE)

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(CONFIG_FILE, "r") as file:
            config: dict[str, str] = json.load(file)
    except FileNotFoundError:
        config = create_default_config()

    match key:
        case "current_vocabulary_id":
            return os.environ.get(
                "VERBIA_VOCABULARY_ID", config.get("current_vocabulary_id")
            )
        case "gemini_api_key":
            return os.environ.get("GEMINI_API_KEY", config.get("gemini_api_key"))
        case _:
            raise ValueError(f"Invalid config key: {key}")


def set_config(key: str, value: str):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    match key:
        case "current_vocabulary_id":
            config["current_vocabulary_id"] = value
        case "gemini_api_key":
            config["gemini_api_key"] = value
        case _:
            raise ValueError(f"Invalid config key: {key}")

    with open(CONFIG_FILE, "w") as f:
        config_json = json.dumps(config, indent=4)
        f.write(config_json)


def create_default_config() -> dict[str, str]:
    with open(CONFIG_FILE, "w") as file:
        file.write(
            json.dumps(
                {},
                indent=4,
            )
        )
    return {}
