# Use the official Python image for a consistent environment
FROM python:3.9.13

# Set the working directory in the container
WORKDIR /app

# Copy requirements first (to take advantage of Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container (code and .env)
COPY . .

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Pydantic will look for .env in the same folder if 'env_file = ".env"'
# (Ensure 'env_file = ".env"' is in your Settings.Config)

# Command to run the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
