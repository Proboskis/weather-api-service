# Weather API Service - Guide and Project Documentation

This repository contains a FastAPI-based Weather API that:

- Fetches weather data asynchronously from OpenWeatherMap (or any external API).
- Caches data locally (or in S3) for 5 minutes to avoid redundant external calls.
- Uploads weather data to S3 (or a local equivalent).
- Logs each event (city, timestamp, S3 URL) to DynamoDB (or a local equivalent).
- Demonstrates asynchronous design, robust error handling, regex validation, and reusable design patterns.

The application can be run locally, in a Docker container, or deployed to AWS Cloud. AWS credentials are used when uploading to actual S3 and logging to DynamoDB.

## Table of Contents

- [Setting up AWS](#setting-up-aws)
  - [IAM Credentials](#iam-credentials)
  - [Creating an S3 Bucket](#creating-an-s3-bucket)
  - [Creating a DynamoDB Table](#creating-a-dynamodb-table)
- [Project Specifications](#project-specifications)
- [Design & Architecture](#design--architecture)
  - [Validators & Design Patterns](#validators--design-patterns)
  - [Caching Mechanism](#caching-mechanism)
- [Local Deployment Without Docker](#local-deployment-without-docker)
- [Local Deployment With Docker](#local-deployment-with-docker)
- [Testing the Service](#testing-the-service)
- [Future Enhancements](#future-enhancements)

---

## Setting up AWS

Before running the project, you need to set up AWS services and credentials.

### IAM Credentials

1. Log in to your **AWS Management Console**.
2. Navigate to **IAM** → **Users** → **Add users**:
   - Check **Programmatic access** (this generates an Access Key ID and Secret Access Key).
3. Attach the following **policies** to the user:
   - `AmazonS3FullAccess`
   - `AmazonDynamoDBFullAccess`
4. Save the generated **Access Key ID** and **Secret Access Key** securely.

> ⚠️ **Note**: Ensure you download the credentials as a `.csv` file from the IAM panel for safekeeping.

### Creating an S3 Bucket

1. Go to **S3** in the AWS Management Console.
2. Click on **Create Bucket**:
   - Choose a unique bucket name, e.g., `weather-data-unique123456`.
   - Select a **region**, e.g., `eu-central-1`.
   - Keep all other settings as default and click **Create bucket**.

### Creating a DynamoDB Table

1. Go to **DynamoDB** in the AWS Management Console.
2. Click **Create table**:
   - Table name: e.g., `weather-logs`.
   - Partition key: `city` (String).
3. Click **Create table** and wait for it to become active.

---

## Project Specifications

This application fulfills the following requirements:

1. **FastAPI Setup**:
   - A single endpoint `/weather` accepts a GET request with a `city` query parameter.
2. **Asynchronous Data Fetching**:
   - Utilizes `httpx.AsyncClient` with proper error handling.
3. **AWS S3 Integration**:
   - Uploads weather data as `{city}_{timestamp}.json` to S3.
4. **AWS DynamoDB Integration**:
   - Logs events (`city`, `timestamp`, `s3_url`) asynchronously.
5. **Caching Mechanism**:
   - Checks the cache directory or S3 for data fetched within the last 5 minutes.
6. **Deployment**:
   - Includes `Dockerfile` and `docker-compose.yml`.

---

## Design & Architecture

### Validators & Design Patterns

- **Validation Strategy**: Ensures that city names only contain letters, spaces, and hyphens (e.g., `New York`, `São Paulo`).
- **Singleton Pattern**: Logger ensures consistent logging throughout the app.
- **Strategy Pattern**: ErrorHandler uses pluggable strategies for error handling.
- **Repository Pattern**: S3Manager and DynamoManager abstract away storage and logging details.

---

### Caching Mechanism

1. **Current Setup**:

   - Data is cached locally in the `cache/` folder.
   - Cache expiration: 5 minutes.
   - Data is also stored in S3, but local cache is checked first.

2. **Future Upgrade**:
   - Fully migrate caching to S3:
     - Replace local file caching with S3-based storage.
     - Use S3 timestamps to manage expiration.

---

## Local Deployment Without Docker

1. **Clone** the repository:

```bash
git clone https://github.com/<your-username>/weather-api-service.git

cd weather-api-service
```

2. Create/activate a Python venv:

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.\.venv\Scripts\activate   # Windows
```

3. **Install dependencies:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Run the application:**

```bash
uvicorn app.main:app --reload
```

5. Open http://127.0.0.1:8000/docs to test the `/weather` endpoint.

## Local Deployment With Docker

1. **Clone** the repository:

```bash
git clone https://github.com/<your-username>/weather-api-service.git

cd weather-api-service
```

2. Create a `.env` file in the root with AWS credentials, etc.:

```bash
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=yyyy
AWS_REGION=eu-central-1
AWS_S3_BUCKET_NAME=weather-data-unique123456
DYNAMODB_TABLE_NAME=weather-logs
OPENWEATHERMAP_API_KEY=abc123 - this is obtained from the openweather api
```

3. **Run Docker Compose**

```bash
docker-compose build
docker-compose up
```

4. The API will run at http://127.0.0.1:8000.

## Testing the Service

1. Open **Swagger UI** at http://127.0.0.1:8000/docs.
2. Test `/weather` with a valid city name, e.g., **London**.
3. Verify:

- **S3**: Check the bucket for `{city}\_{timestamp}.json`.
- **DynamoDB**: Check the table for the log entry.
- **Local Cache**: The `cache/` folder should have `{city}.json`.

## Future Enhancements

1. Fully Migrate to S3 Cache: Replace local caching logic with S3 for distributed scalability.
2. LocalStack Integration: For purely local dev with S3/DynamoDB mocks.
3. Advanced Caching: Redis or Memcached integration.
4. Authentication: Add JWT or OAuth2 to secure the endpoint.

> [!NOTE]
> Worthy information of note:
> Also for a future full-stack application it could be of great benefit to use Github CI/CD actions or Jenkins to automate the softvare development lifecycle.
> Kubernetes could be used together with docker, should the application expand, and should there be a need to orchestrate many containers.
> An Angular, or a React (preferably Next.js) frontend can be built out.
> Unit testing for both backedn and frontend...
