# File: app/aws/s3_manager.py

import asyncio
import aioboto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

from app.validators.city_validation import CityNameValidationStrategy
from app.utils.logger import Logger
from app.utils.error_handler import ErrorHandler, LogErrorStrategy
from app.config.settings import settings

logger = Logger.get_logger()

class S3Manager:
    """Manager class for S3 operations."""

    def __init__(self):
        self.bucket_name = settings.aws_s3_bucket_name
        self.region = settings.aws_region
        self.city_validator = CityNameValidationStrategy()

    @ErrorHandler.handle_error(LogErrorStrategy.handle)
    async def save_weather_data(self, city: str, data: dict) -> str:
        """
        Asynchronously save weather data to an S3 bucket and return the S3 URL.
        Raises exceptions on failure, letting the error handler produce a consistent
        error response (instead of returning a dict).
        """
        # Validate city name
        self.city_validator.validate(city)

        session = aioboto3.Session()
        retries = 1
        for attempt in range(retries):
            try:
                logger.info(f"Starting upload for city: {city}")

                timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
                filename = f"{city}_{timestamp}.json"
                json_data = json.dumps(data)

                async with session.client("s3", region_name=self.region) as s3_client:
                    logger.debug(f"Uploading to bucket: {self.bucket_name}, key: {filename}")
                    await s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=filename,
                        Body=json_data,
                        ContentType="application/json",
                    )

                s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
                logger.info(f"Successfully uploaded {city} data to S3: {s3_url}")
                return s3_url

            except ClientError as e:
                logger.error(f"S3 ClientError during upload for {city}: {e}")
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(1)

            except Exception as e:
                logger.critical(f"Unexpected error during upload for {city}: {e}")
                raise
