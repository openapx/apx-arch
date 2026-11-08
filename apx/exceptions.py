"""
Standard exceptions 
"""

class InvalidConfigurationException(Exception):
    """Exception raised for missing or invalid configuration."""

    def __init__(self, message="Invalid configuration"):
        self.message = message
        super().__init__(self.message)

