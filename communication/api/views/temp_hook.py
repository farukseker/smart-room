from discord import SyncWebhook
from config.settings.base_settings import env
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from datetime import datetime

ESP_USER_COM = env('ESP_USER_COM')
API_KEY = env("ESP_TEMP_API_KEY")


@csrf_exempt
def send_discord(request):
    if request.method == "POST":
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        try:
            webhook = SyncWebhook.from_url(ESP_USER_COM)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            webhook.send(f"[{now}] ESP motion detected!")
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=405)
