"""
Objects and functions to manage app and API configuration
"""


from dataclasses import dataclass, field

import os
import re
import apx.exceptions


def apphome() -> str:
    """
    Get the app home environment variable configuration value

    :return: The directory path of the app home environment variable
    :rtype: str

    :raises ConfigurationException: If the app home environment variable is not set
    :raises ConfigurationException: If multiple app home environmental variables are set
    :raises ConfigurationException: If the path specified by app home is not an existing directory
    """

    # -- app home environment 

    env_home : dict[str, str] = {}

    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            env_home[key] = value.strip()

    if len(env_home) == 0:
        raise apx.exceptions.ConfigurationException("App home environment variable is not set")

    if len(env_home) > 1:
        raise apx.exceptions.ConfigurationException("Multiple app home environment variables are set")

    # -- determine the app home directory
    app_home = list(env_home.values())[0]

    if not os.path.isdir(app_home):
        raise apx.exceptions.ConfigurationException("App home directory does not exist or is not a directory")


    # -- return the app home envioronmental variable value
    return app_home



def load_properties( path: str ) -> dict[str, str]:
    """
    Load properties from a file at the specified path

    :param path: The path to the properties file
    :type path: str

    :return: A dictionary containing the properties as key-value pairs
    :rtype: dict[str, str]

    :raises ConfigurationException: If the properties file does not exist
    :raises ConfigurationException: If the properties file cannot be read or parsed  
    :raises ConfigurationException: If a property name is in an invalid format
    """


    if not path or not os.path.isfile(path):
        raise apx.exceptions.ConfigurationException("Properties file does not exist")

    with open(path, "r") as f:
        lines = f.readlines()

    properties: dict[str, str] = {}

    for line in lines:

        # - ignore empty lines or comments (first non-blank character is '#')
        if not line.strip() or line.strip().startswith("#"):
            continue

        # - key-value delimiter is equal sign '='
        if "=" not in line.strip():
            raise apx.exceptions.ConfigurationException(f"Property definition missing equal sign")

        # - split the line into key and value at the first equal sign   
        key, value = line.split("=", 1) 

        if not re.match(r"^[a-z0-9]([.]?[a-z0-9]+)+$", key.strip().lower()):
            raise apx.exceptions.ConfigurationException("Invalid property name")

        if key.strip().lower() in properties:
            raise apx.exceptions.ConfigurationException("Duplicate property definition")

        # - register property
        properties[key.strip().lower()] = value.strip()


    return properties
    

@dataclass(frozen=True)
class AppConfiguration:

    # -- internal dictionary to store configuration attributes
    _attr: dict[str, str] = field(default_factory=dict)

    # -- housekeeping attributes
    _apphome: str | None = None
    _propfiles: list[str] = field(default_factory=list)


    @property
    def apphome(self) -> str | None:
        return self._apphome

    @property
    def files(self) -> list[str]:
        return self._propfiles


    def __post_init__(self):

        # -- skip initialization if attributes are already set
        if self._attr:
            return

        # -- configuration in app home
        object.__setattr__(self, "_apphome", apphome())

        if not os.path.isdir(os.path.join(self._apphome, "config")):
            raise apx.exceptions.ConfigurationException("App home config directory does not exist")


        # -- identify property files
        prop_files: list[str] = []

        for file_name in os.listdir(os.path.join(self._apphome, "config")):
            if file_name.lower().endswith(".properties"):
                prop_files.append(os.path.join(self._apphome, "config", file_name))

        object.__setattr__(self, "_propfiles", sorted(prop_files))

        if not prop_files:
            return

        # -- load properties from identified files
        props: dict[str, str] = {}

        for prop_file in self._propfiles:

            # - read properties from file
            fprops = load_properties(prop_file)

            for key, value in fprops.items():
                if key in props:
                    raise apx.exceptions.ConfigurationException("Duplicate property definition across identified property files")
                
                props[key] = value.strip()

        # -- initialise internal attribute dictionary with loaded properties
        object.__setattr__(self, "_attr", props)
        

    
    def __call__(self, key: str, default: str | None = None) -> str | None:
        """Retrieve the value of a configuration property.

        :param key: The property key to look up.
        :type key: str
        :param default: The default value to return if the key is not found. Defaults to None.
        :type default: str | None

        :return: The value of the property if found, otherwise the default value.
        """

        if not isinstance(key, str):
            raise TypeError("Configuration key must be a string")

        return self._attr.get(key.strip().lower(), default)



        

