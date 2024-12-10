from pydantic_settings import BaseSettings, SettingsConfigDict


class ClickPyDataBaseSetting(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='CLICKPY_',
        extra='ignore',
    )

    HOST: str = 'https://sql-clickhouse.clickhouse.com'
    SECURE: bool = True
    USERNAME: str = 'play'
    PASSWORD: str = ''


CLICK_PY_DATA_BASE_SETTING = ClickPyDataBaseSetting()
