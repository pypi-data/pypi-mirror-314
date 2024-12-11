import requests
import json
from requests.auth import HTTPBasicAuth
from rich import print
from typing import Optional


class GrafanaDashboard:
    grafana_url = "http://localhost:8000"
    username = "admin"
    password = "pass"

    def __init__(self):
        """
        Initialize the uploader with Grafana server details and credentials.
        """
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {"Content-Type": "application/json"}

    def upload_dashboard(
        self, json_file_path: str, dashboard_name: str, folder_uid: Optional[str] = None
    ) -> bool:
        """
        Upload a dashboard to Grafana.

        :param json_file_path: Path to the JSON file containing the dashboard definition
        :param dashboard_name: Desired name for the dashboard in Grafana
        :param folder_uid: UID of the folder to save the dashboard in (optional)
        :return: True if upload was successful, False otherwise
        """
        try:
            with open(json_file_path, "r") as file:
                dashboard_json = json.load(file)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return False

        # Update the dashboard title
        dashboard_json["title"] = dashboard_name

        # Prepare the payload
        payload = {"dashboard": dashboard_json, "overwrite": True}

        if folder_uid:
            payload["folderUid"] = folder_uid

        # Send the request to Grafana
        response = requests.post(
            f"{self.grafana_url}/api/dashboards/db",
            headers=self.headers,
            auth=self.auth,
            data=json.dumps(payload),
        )

        if response.status_code == 200:
            print(f"Dashboard '{dashboard_name}' uploaded successfully.")
            return True
        else:
            print(
                f"Failed to upload dashboard. Status code: {response.status_code}, Response: {response.text}"
            )
            return False

    def delete_dashboard(self, dashboard_uid: str) -> bool:
        """
        Delete a dashboard by its UID.

        :param dashboard_uid: UID of the dashboard to delete
        :return: True if deletion was successful, False otherwise
        """
        response = requests.delete(
            f"{self.grafana_url}/api/dashboards/uid/{dashboard_uid}",
            headers=self.headers,
            auth=self.auth,
        )

        if response.status_code == 200:
            print(f"Dashboard with UID '{dashboard_uid}' deleted successfully.")
            return True
        else:
            print(
                f"Failed to delete dashboard. Status code: {response.status_code}, Response: {response.text}"
            )
            return False

    def get_dashboard_uid_by_name(self, dashboard_name: str) -> Optional[str]:
        """
        Retrieve the UID of a dashboard by its name.

        :param dashboard_name: Name of the dashboard
        :return: UID of the dashboard if found, None otherwise
        """
        search_response = requests.get(
            f"{self.grafana_url}/api/search",
            headers=self.headers,
            auth=self.auth,
            params={"query": dashboard_name},
        )

        if search_response.status_code == 200:
            for item in search_response.json():
                if (
                    item.get("title") == dashboard_name
                    and item.get("type") == "dash-db"
                ):
                    return item.get("uid")
            print(f"Dashboard with name '{dashboard_name}' not found.")
        else:
            print(
                f"Failed to search dashboards. Status code: {search_response.status_code}, Response: {search_response.text}"
            )
        return None
