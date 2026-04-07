import os
import tomllib
from pathlib import Path

import platformdirs

CONFIG_DIR = Path(platformdirs.user_config_dir("kindleify"))
CONFIG_FILE = CONFIG_DIR / "config.toml"


def load_config() -> dict:
    """Load config from file, return empty dict if not found."""
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def save_config(config: dict):
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    for section, values in config.items():
        if isinstance(values, dict):
            lines.append(f"[{section}]")
            for key, value in values.items():
                lines.append(f'{key} = "{value}"')
            lines.append("")
    with open(CONFIG_FILE, "w") as f:
        f.write("\n".join(lines))


def get_kindle_config() -> dict:
    """Get Kindle-specific config (kindle section)."""
    config = load_config()
    return config.get("kindle", {})


def set_kindle_config(to_email: str, from_email: str, password: str):
    """Save Kindle credentials to config."""
    config = load_config()
    config["kindle"] = {
        "to_email": to_email,
        "from_email": from_email,
        "password": password,
    }
    save_config(config)


def clear_kindle_config():
    """Remove Kindle credentials from config."""
    config = load_config()
    if "kindle" in config:
        del config["kindle"]
        save_config(config)


def has_kindle_config() -> bool:
    """Check if Kindle credentials are configured."""
    cfg = get_kindle_config()
    return bool(cfg.get("to_email") and cfg.get("from_email") and cfg.get("password"))
