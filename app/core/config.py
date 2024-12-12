from typing import List

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SENTRY_DSN: str = ''
    ENV: str = ''
    OPENAPI_URL: str = ''

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24
    SECRET_KEY: str = 'secret'
    ALGORITHM: str = 'HS256'

    USER_SUB_WEBHOOK: str = 'http://localhost:8000/api/v1/webhook/'

    DS1_BASE_URL: str = 'https://credcompare-hr-test-d81ffdfbad0d.herokuapp.com'
    DS1_SUBSCRIBE: str = '/subscribe/{stream}'
    DS1_RETRIEVE: str = '/stream/'
    DS1_AVAILABLE_TOPICS: List[str] = ["golf", "news", "food", "movies", "hobby", "games"]
    DS1_DESCRIPTION: str = 'Some source description'

    DS2_BASE_URL: str = 'https://credcompare-hr-test-d81ffdfbad0d.herokuapp.com'
    DS2_SUBSCRIBE: str = '/subscribe/{stream}'
    DS2_RETRIEVE: str = '/stream/'
    DS2_AVAILABLE_TOPICS: List[str] = ["golf", "news", "food", "movies", "hobby", "games"]
    DS2_DESCRIPTION: str = 'Some source description'

    # mongo
    MONGO_CONNECTION_URI: str
    USE_MONGO_MOCK: bool = True

    class Config:
        case_sensitive = True


settings = Settings()
