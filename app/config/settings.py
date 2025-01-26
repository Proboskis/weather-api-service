from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Weather API Service"
    log_level: str = "INFO"
    openweathermap_api_key: str
    aws_region: str
    aws_s3_bucket_name: str
    dynamodb_table_name: str

    class Config:
        env_file = ".env"

settings = Settings()
