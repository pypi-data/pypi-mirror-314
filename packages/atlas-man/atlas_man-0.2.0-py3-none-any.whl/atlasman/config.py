"""
Configuration module for Atlas-Man CLI.

This module provides functionality to manage the configuration file located at
~/.config/atlas-man/config.json. The configuration includes API tokens and default
settings for both Trello and Jira integrations, as well as CLI preferences.
"""

import json
import os
from typing import Any, Dict, Optional

# Define the path to the configuration file
CONFIG_DIR = os.path.expanduser("~/.config/atlas-man")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Default configuration template
DEFAULT_CONFIG = {
    "trello": {
        "api_key": "",
        "api_secret": "",
        "oauth_token": "",
        "alias_ids": {
            "shopping": {
                "board_id": "",
                "list_id": ""
            },
            "todo": {
                "board_id": "",
                "list_id": ""
            }
        }
    },
    "jira": {
        "api_token": "",
        "base_url": "https://yourdomain.atlassian.net",
        "username": "",
        "default_project_key": "",
        "default_issue_type": "",
        "show_done_issues": False,
        "custom_status_order": {
            "To Do": 1,
            "In Progress": 2,
            "Testing": 3,
            "Done": 4
        }
    },
    "cli": {
        "verbose": False,
        "default_tool": "trello",
        "output_format": "json"
    }
}

def edit_config() -> None:
    """
    Open the configuration file in the default editor for manual editing.
    """
    os.system(f"{os.getenv('EDITOR', 'vi')} {CONFIG_FILE}")

def load_config() -> Dict[str, Any]:
    """
    Load the configuration file. If the file does not exist, create it with default values.
    If the file is malformed, prompt the user to fix it or reset to default.

    Returns:
        Dict[str, Any]: A dictionary with configuration settings.
    """

    if not os.path.exists(CONFIG_FILE):
        print(f"Configuration file not found. Creating a new one at {CONFIG_FILE}.")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # Check if config is complete; if not, update with defaults
        return _update_with_defaults(config)
    except json.JSONDecodeError as exc:
        print("Error: The configuration file is malformed.")
        choice = input(
            "Would you like to reset the configuration to default? (y/n): ").strip().lower()
        if choice == 'y':
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        else:
            raise ValueError(
                f"Please correct the configuration file format at {CONFIG_FILE}") from exc

def save_config(config: Dict[str, Any]) -> None:
    """
    Save the configuration dictionary to the configuration file in JSON format.
    Ensure that the configuration directory exists before saving.

    Args:
        config (Dict[str, Any]): The configuration dictionary to be saved.
    """
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {CONFIG_FILE}.")

def _update_with_defaults(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a configuration dictionary with missing default values.
    
    Args:
        config (Dict[str, Any]): The configuration dictionary to check and update.

    Returns:
        Dict[str, Any]: The updated configuration dictionary with default values filled in.
    """

    updated_config = DEFAULT_CONFIG.copy()
    for section, defaults in DEFAULT_CONFIG.items():
        if section in config:
            if isinstance(config[section], dict):
                # Only update missing keys within the section
                updated_config[section].update(
                    {k: config[section].get(k, v) for k, v in defaults.items()})
            else:
                print(f"Warning: Expected '{section}' to be a dictionary, resetting to default.")
        else:
            print(f"Warning: Missing configuration section '{section}', adding default.")
    updated_config.update(config)

    if updated_config != config:
        save_config(updated_config)
    return updated_config

def get_config_value(section: str, key: str) -> Optional[Any]:
    """
    Retrieve a specific value from the configuration.

    Args:
        section (str): The configuration section (e.g., 'trello', 'jira', 'cli').
        key (str): The key within the section to retrieve (e.g., 'api_key').

    Returns:
        Optional[Any]: The configuration value if it exists, otherwise None.
    """
    config = load_config()
    return config.get(section, {}).get(key)

def set_config_value(section: str, key: str, value: Any) -> None:
    """
    Set a specific value in the configuration and save it.

    Args:
        section (str): The configuration section (e.g., 'trello', 'jira', 'cli').
        key (str): The key within the section to set (e.g., 'api_key').
        value (Any): The value to set in the configuration.
    """
    config = load_config()
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config(config)
