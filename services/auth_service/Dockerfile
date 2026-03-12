# Dockerfile for auth_service
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --without dev
COPY . .
CMD ["python", "-m", "django", "runserver", "0.0.0.0:8000"]
