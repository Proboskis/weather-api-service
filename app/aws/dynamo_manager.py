# File: app/aws/dynamo_manager.py

import asyncio
import aioboto3
from botocore.exceptions import ClientError
from app.utils.logger import Logger
from app.utils.error_handler import ErrorHandler, LogErrorStrategy
from app.config.settings import settings

logger = Logger.get_logger()

class DynamoManager:
    def __init__(self):
        self.region = settings.aws_region
        self.table_name = settings.dynamodb_table_name

    @ErrorHandler.handle_error(LogErrorStrategy.handle)
    async def log_event(self, city: str, timestamp: str, s3_url: str) -> None:
        """
        Asynchronously log weather data to DynamoDB with a basic retry mechanism.
        Uses a session-based approach for older aioboto3 versions that may not
        support aioboto3.client(...) at the top level.
        """
        retries = 1
        for attempt in range(retries):
            try:
                # Create an aioboto3 session
                session = aioboto3.Session()

                async with session.client("dynamodb", region_name=self.region) as dynamo_client:
                    logger.info(
                        f"Attempting to log data to DynamoDB for city: {city}, timestamp: {timestamp}"
                    )
                    await dynamo_client.put_item(
                        TableName=self.table_name,
                        Item={
                            "city": {"S": city},
                            "timestamp": {"S": timestamp},
                            "s3_url": {"S": s3_url},
                        },
                    )
                    logger.info(f"Successfully logged data for city: {city} to DynamoDB.")

                return  # Exit on success

            except ClientError as e:
                logger.error(f"ClientError encountered when logging data for city {city}: {e}")
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(1)

            except Exception as e:
                logger.critical(f"Unexpected error encountered when logging data for city {city}: {e}")
                raise
