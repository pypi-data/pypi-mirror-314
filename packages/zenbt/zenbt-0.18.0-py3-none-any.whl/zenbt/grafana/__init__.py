import requests
import json
from requests.auth import HTTPBasicAuth
from rich import print
from pydantic import BaseModel, ConfigDict
from typing import Optional

from .token_manager import TokenManager
from .dashboard import GrafanaDashboard


# Initialize the manager with Grafana server details and admin credentials
# manager = TokenManager()
# manager.get_key()


# Initialize the uploader with Grafana server details and credentials
uploader = GrafanaDashboard()

BASE_URL = "./src/grafana"
json_file_path = f"{BASE_URL}/dashboard.json"
dashboard_name = "Backtest Dashboard"  # Desired name for the dashboard in Grafana
folder_uid = None


def ohlc():
    with open(f"{BASE_URL}/dashboard.json", "r") as file:
        dash = file.read()
        dash = json.loads(dash)

    with open(f"{BASE_URL}/echarts.js", "r") as file:
        script = file.read()

    dash["panels"][0]["options"]["getOption"] = script

    with open(f"{BASE_URL}/dashboard.json", "w") as file:
        json.dump(dash, file, indent=4)

    uploader.upload_dashboard(json_file_path, dashboard_name, folder_uid)
