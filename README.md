# Weather API Service

This is a FastAPI-based Weather API that:

- Fetches weather data asynchronously from OpenWeatherMap (or any external API).
- Stores JSON responses in S3 (or local equivalent).
- Logs events to DynamoDB (or local equivalent).
- Maintains a 5-minute cache for weather data.

## Features

1. **Asynchronous** FastAPI endpoints for better concurrency and high traffic handling.
2. **S3Manager** to upload JSON data (`city_timestamp.json`) to S3.
3. **DynamoManager** to log events (city, timestamp, S3 URL) to DynamoDB.
4. **CacheManager** to check if weather data exists before refetching.
5. **Singleton Logger** for consistent logging, following design patterns (Strategy for error handling, Singleton for logger).
6. **.env** and **Pydantic** for environment-based configuration.

## Setup Instructions

### 1. Local Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app (developer mode)
uvicorn app.main:app --reload
```
