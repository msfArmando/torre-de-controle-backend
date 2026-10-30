from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    ENVIRONMENT: str = ""
    DATABASE_URL_ORACLE: str = ""
    ENVIRONMENT_ORACLE: str = ""
    PANTERA_TOKEN: str = ""
    PANTERA_URL: str = "https://maestro.umgrauemeio.com/api/client/reports"
    URL_TEBE: str = ""
    API_KEY_TEBE_USICODA: str = ""
    API_KEY_TEBE_COMVAP: str = ""
    API_KEY_TEBE_GIASA: str = ""
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:5501", "http://127.0.0.1:5501"]

    DB_HOST: str = ""
    DB_PORT: int = 1521
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASS: str = ""

    DB_USER_IONICS: str = ""
    DB_PASS_IONICS: str = ""

    MYSQL_DB_HOST: str = ""
    MYSQL_DB_PORT: int = ""
    MYSQL_DB_NAME: str = ""
    MYSQL_DB_USER: str = ""
    MYSQL_DB_PASS: str = ""   

    class Config:
        env_file = ".env"

settings = Settings()