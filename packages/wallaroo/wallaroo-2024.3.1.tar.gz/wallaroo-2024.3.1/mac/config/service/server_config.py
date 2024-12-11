"""This module features the ServerConfig class, for specifying the server
configuration."""

from ipaddress import IPv4Address

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    """This class implements the ServerConfig class, for specifying the connection
    configuration for a server."""

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    # the host to serve the model on
    host: str = "0.0.0.0"

    # the port to serve the model on
    port: int = 8080

    # whether to use a lock to synchronize access to `PythonStep`
    use_lock: bool = True

    @field_validator("host")
    @classmethod
    def validate_host(cls, value):
        """Validate host."""
        try:
            IPv4Address(value)
            return value
        except ValueError as error:
            raise ValueError("Invalid IP address") from error

    @field_validator("port")
    @classmethod
    def validate_port(cls, value):
        """Validate port."""
        if not isinstance(value, int) or value <= 0 or value > 65535:
            raise ValueError("Invalid port number")
        return value
