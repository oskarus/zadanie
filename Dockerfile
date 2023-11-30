# Base stage: Common image for all stages
FROM --platform=$BUILDPLATFORM python:3.10.13-slim AS base

# Builder stage: Compile and prepare the application
FROM base AS builder
ARG TARGETPLATFORM
ARG BUILDPLATFORM

WORKDIR /app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --compile -r requirements.txt
COPY ./app .

# Development stage
FROM builder AS development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM builder AS production
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
