import requests
import os

# Environment variable for Render URL
RENDER_URL = os.getenv("RENDER_URL", "https://file-receiver-bot.onrender.com/")

def handler(request):
    try:
        response = requests.get(RENDER_URL)
        print(f"Render app response: {response.status_code}")
    except Exception as e:
        print(f"Error pinging Render app: {e}")

    return "Pinging Render app", 200
