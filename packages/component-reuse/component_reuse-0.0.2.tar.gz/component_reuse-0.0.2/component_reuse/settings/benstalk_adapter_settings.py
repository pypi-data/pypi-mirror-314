from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class BeanstalkAdapterSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/workspace/liferaft-python-lib/.devcontainer/.env", extra="allow"
    )
    BEANSTALK_HOST: str
    BEANSTALK_PORT: int
    BEANSTALK_QUEUE_NAME: str


# Instantiate settings
beanstalk_adapter_settings = BeanstalkAdapterSettings()
