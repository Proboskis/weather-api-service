# File: app/validators/city_validation.py

import re

from app.validators.base_strategy import ValidationStrategy
from app.utils.logger import Logger

logger = Logger.get_logger()

class CityNameValidationStrategy(ValidationStrategy):
    """
    Concrete validation strategy for city names. 
    Allows letters (including accented), spaces, and hyphens, e.g. "New York", "São-Paulo".
    """
    
    CITY_NAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$')

    def validate(self, city: str) -> None:
        """Raise ValueError if city is invalid."""
        if not city or not CityNameValidationStrategy.CITY_NAME_PATTERN.match(city):
            logger.error(f"Invalid city name: {city}")
            raise ValueError(f"Invalid city name: {city}")
