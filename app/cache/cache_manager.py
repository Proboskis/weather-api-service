# File: app/cache/cache_manager.py

import os
import json
import aiofiles
from typing import Optional
from datetime import datetime, timedelta
from app.validators.city_validation import CityNameValidationStrategy
from app.utils.logger import Logger
from app.utils.error_handler import ErrorHandler, LogErrorStrategy

logger = Logger.get_logger()

CACHE_DIR = "cache"
CACHE_EXPIRY_MINUTES = 5

os.makedirs(CACHE_DIR, exist_ok=True)

class CacheManager:
    """Provides caching functionality for weather data."""

    def __init__(self):
        # We instantiate (or store) our city validator
        self.city_validator = CityNameValidationStrategy()

    @ErrorHandler.handle_error(LogErrorStrategy.handle)
    async def get_cached_weather(self, city: str) -> Optional[dict]:
        logger.info(f"Retrieving cached weather data for city: {city}")
        
        # Use the shared city validator
        try:
            self.city_validator.validate(city)
        except ValueError:
            logger.warning(f"Invalid city name format: {city}")
            return None

        file_path = os.path.join(CACHE_DIR, f"{city}.json")
        if not os.path.exists(file_path):
            logger.info(f"No cache file found for city: {city}")
            return None

        # Read JSON file asynchronously
        async with aiofiles.open(file_path, "r") as file:
            data = json.loads(await file.read())

        # Check timestamp
        timestamp_str = data.get("timestamp")
        if not timestamp_str:
            logger.warning(f"No valid timestamp found in the cache for city: {city}")
            return None

        timestamp = datetime.fromisoformat(timestamp_str)
        if datetime.utcnow() - timestamp < timedelta(minutes=CACHE_EXPIRY_MINUTES):
            logger.info(f"Cache for city {city} is still valid.")
            return data.get("weather")

        logger.info(f"Cache for city {city} has expired.")
        return None

    @ErrorHandler.handle_error(LogErrorStrategy.handle)
    async def cache_weather(self, city: str, data: dict) -> None:
        logger.info(f"Saving weather data to cache for city: {city}")

        # Validate city name to keep it consistent
        self.city_validator.validate(city)

        file_path = os.path.join(CACHE_DIR, f"{city}.json")
        data_to_save = {
            "timestamp": datetime.utcnow().isoformat(),
            "weather": data
        }

        async with aiofiles.open(file_path, "w") as file:
            await file.write(json.dumps(data_to_save))

        logger.info(f"Weather data for {city} successfully saved to cache.")
