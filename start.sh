#!/bin/bash
pip install -r requirements.txt
gunicorn config.asgi:application DJANGO_SETTINGS_MODULE=config.settings.product -k uvicorn.workers.UvicornWorker --log-file -
