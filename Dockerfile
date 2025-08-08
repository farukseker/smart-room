FROM python:3.9-slim

WORKDIR /app

COPY requirements.latest.txt .
RUN pip install --no-cache-dir -r requirements.latest.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings.product \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--chdir", "/app", \
     "config.asgi:application", \
     "--worker-class", "uvicorn.workers.UvicornWorker"]