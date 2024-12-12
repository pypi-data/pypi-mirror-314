from pydantic_settings import BaseSettings, SettingsConfigDict

from sila import cloud_connector, server


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__", extra="ignore"
    )

    environment: str = "development"
    sila_server: server.ServerConfig = server.ServerConfig()
    cloud_server_endpoint: cloud_connector.CloudServerEndpointConfig = cloud_connector.CloudServerEndpointConfig()
