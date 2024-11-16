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

    rm_user: str
    rm_pass: str
    rm_args: str

    @property
    def database_url(self) -> str:
        return f'{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_port}/{self.db_name}'

    @property
    def get_redis_url(self) -> str:
        return f'{self.redis_user}://{self.redis_user}:{self.redis_port}'

    @property
    def get_url_currency_exchange_rate(self) -> str:
        return self.api_course

    model_config = SettingsConfigDict(env_file="../../.env")


settings = Settings()

if __name__ == '__main__':
    n = settings
    print(n.dict())
    print(n.get_url_currency_exchange_rate)
