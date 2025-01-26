# File: app/routers/weather.py
from fastapi import APIRouter, Query
from app.services.weather_service import WeatherService
from app.utils.error_handler import ErrorHandler, LogErrorStrategy
from app.utils.logger import Logger

class WeatherRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/weather", tags=["Weather"])
        self.logger = Logger.get_logger()
        self.weather_service = WeatherService()
        self.handle_error = ErrorHandler.handle_error(LogErrorStrategy.handle)

        # Attach route and wrap `get_weather` with the error handler.
        self.router.add_api_route(
            "/",
            self.handle_error(self.get_weather),
            methods=["GET"]
        )

    async def get_weather(self, city: str = Query(..., description="City name to fetch weather")):
        """
        Fetch weather data for the given city as a query parameter:
          /weather?city=London  for example ...
        """
        self.logger.info(f"Received request for city: {city}")
        weather_data = await self.weather_service.get_weather(city)
        return {"message": "Success", "data": weather_data}

# Router instance for main.py
router = WeatherRouter().router
