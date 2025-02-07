from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_driver: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    time_zone: str

    redis_user: str
    redis_port: int

    api_course: str

    rm_driver: str
    rm_user: str
    rm_pass: str
    rm_args: str
    rm_host: str
    rm_local_port: str

    @property
    def database_url(self) -> str:
        return f'{self.db_name}+{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_port}/{self.db_name}'

    @property
    def get_redis_url(self) -> str:
        return f'{self.redis_user}://{self.redis_user}:{self.redis_port}'

    @property
    def get_url_currency_exchange_rate(self) -> str:
        return self.api_course

    @property
    def get_rabbitmq_url(self):
        return f'{self.rm_driver}://{self.rm_user}:{self.rm_pass}@{self.rm_host:{self.rm_local_port}}'

    model_config = SettingsConfigDict(env_file="../../.env")


settings = Settings()
