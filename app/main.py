# File: app/main.py
from fastapi import FastAPI
from app.routers.weather import router as weather_router
from app.utils.logger import Logger
from app.utils.error_handler import ErrorHandler, LogErrorStrategy
from app.config.settings import settings

class Application:
    @ErrorHandler.handle_error_sync(LogErrorStrategy.handle)
    def __init__(self):
        self.app = FastAPI(title=settings.app_name)
        self.logger = Logger.get_logger()

    @ErrorHandler.handle_error_sync(LogErrorStrategy.handle)
    def configure_routes(self):
        self.app.include_router(weather_router)

    @ErrorHandler.handle_error_sync(LogErrorStrategy.handle)
    def run(self):
        self.logger.info(f"{settings.app_name} starting...")
        self.configure_routes()
        self.logger.info(f"{settings.app_name} started.")
        return self.app

app_instance = Application()
app = app_instance.run()
