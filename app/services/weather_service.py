# File: app/services/weather_service.py
from datetime import datetime
import asyncio
from httpx import AsyncClient
from app.aws.s3_manager import S3Manager
from app.aws.dynamo_manager import DynamoManager
from app.cache.cache_manager import CacheManager
from app.config.settings import settings
from app.utils.logger import Logger

logger = Logger.get_logger()

class WeatherService:
    def __init__(self):
        self.s3_manager = S3Manager()
        self.dynamo_manager = DynamoManager()
        self.cache_manager = CacheManager()

    async def get_weather(self, city: str):
        logger.info(f"Fetching weather data for city: {city}")
        # Check cache
        cached_data = await self.cache_manager.get_cached_weather(city)
        if cached_data:
            logger.info(f"Cache hit for city: {city}")
            return cached_data

        logger.info(f"Cache miss for city: {city}. Fetching from external API.")
        # Fetch from external API
        weather_data = await self.fetch_weather_from_api(city)

        # Store in cache, S3, and log to DynamoDB
        s3_url = await self.s3_manager.save_weather_data(city, weather_data)

        # Generate a timestamp for DynamoDB
        timestamp = datetime.utcnow().isoformat()

        # Log event to DynamoDB with (city, timestamp, s3_url)
        await self.dynamo_manager.log_event(city, timestamp, s3_url)

        # Cache the weather data
        await self.cache_manager.cache_weather(city, weather_data)

        return weather_data

    async def fetch_weather_from_api(self, city: str):
        """Fetch weather data from external API asynchronously."""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.openweathermap_api_key}"
        retries = 1

        async with AsyncClient() as client:
            for attempt in range(retries):
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.json()
                except Exception as e:
                    if attempt == retries - 1:
                        logger.error(f"Failed to fetch data for {city}: {e}")
                        raise
                    await asyncio.sleep(1)
