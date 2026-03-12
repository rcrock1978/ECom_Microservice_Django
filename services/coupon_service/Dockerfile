# Dockerfile for coupon_service
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY . .
CMD ["uvicorn", "coupon_service.wsgi:application", "--host", "0.0.0.0", "--port", "8000"]
