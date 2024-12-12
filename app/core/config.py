from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SENTRY_DSN: str = ''
    ENV: str = ''
    OPENAPI_URL: str = ''

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24
    SECRET_KEY: str = 'secret'
    ALGORITHM: str = 'HS256'

    # mongo
    MONGO_CONNECTION_URI: str

    class Config:
        case_sensitive = True


settings = Settings()
