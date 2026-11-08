"""
Objects and functions to manage app and API configuration
"""


from dataclasses import dataclass, field

import os
import apx.exceptions


async def apphome() -> str:
    """
    Get the app home environment variable configuration value

    :return: The directory path of the app home environment variable
    :rtype: str

    :raises InvalidConfigurationException: If the app home environment variable is not set
    :raises InvalidConfigurationException: If multiple app home environmental variables are set
    :raises InvalidConfigurationException: If the path specified by app home is not an existing directory
    """

    # -- app home environment 

    env_home : dict[str, str] = {}

    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            env_home[key] = value.strip()

    if len(env_home) == 0:
        raise apx.exceptions.InvalidConfigurationException("App home environment variable is not set")

    if len(env_home) > 1:
        raise apx.exceptions.InvalidConfigurationException("Multiple app home environment variables are set")

    # -- determine the app home directory
    app_home = list(env_home.values())[0]

    if not os.path.isdir(app_home):
        raise apx.exceptions.InvalidConfigurationException("App home directory does not exist or is not a directory")


    # -- return the app home envioronmental variable value
    return app_home

