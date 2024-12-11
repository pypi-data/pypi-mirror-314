import requests
import json
from requests.auth import HTTPBasicAuth
from rich import print
from pydantic import BaseModel, ConfigDict


class TokenManager(BaseModel):
    admin_user: str = "admin"
    admin_password: str = "pass"
    grafana_url: str = "http://localhost:8000"
    service_account_name: str = "my_account"
    service_account_token_name: str = "my_token"

    auth: HTTPBasicAuth = HTTPBasicAuth("", "")
    headers: dict = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def create_service_account(self):
        """
        Create a new service account.

        :param name: Desired name for the service account
        :param role: Role for the service account ('Viewer', 'Editor', or 'Admin')
        :return: Dictionary containing service account details or None if creation failed
        """
        payload = {"name": self.service_account_name, "role": "Admin"}
        response = requests.post(
            f"{self.grafana_url}/api/serviceaccounts",
            headers=self.headers,
            auth=self.auth,
            data=json.dumps(payload),
        )
        if response.status_code == 201:
            return response.json()
        else:
            print(
                f"Failed to create service account. Status code: {response.status_code}, Response: {response.text}"
            )
            return None

    def generate_service_account_token(self, service_account_id, token_name):
        """
        Generate a token for an existing service account.

        :param service_account_id: ID of the service account
        :param token_name: Desired name for the token
        :return: Dictionary containing token details or None if generation failed
        """
        payload = {"name": token_name}
        response = requests.post(
            f"{self.grafana_url}/api/serviceaccounts/{service_account_id}/tokens",
            headers=self.headers,
            auth=self.auth,
            data=json.dumps(payload),
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to create service account token. Status code: {response.status_code}, Response: {response.text}"
            )
            return None

    def get_service_account_id_by_name(self):
        """
        Retrieve the ID of a service account by its name.

        :param name: Name of the service account
        :return: Service account ID if found, None otherwise
        """
        response = requests.get(
            f"{self.grafana_url}/api/serviceaccounts/search",
            headers=self.headers,
            auth=self.auth,
            params={"query": self.service_account_name},
        )
        if response.status_code == 200:
            accounts = response.json().get("serviceAccounts", [])
            for account in accounts:
                if account["name"] == self.service_account_name:
                    return account["id"]
            print(f"Service account with name '{self.service_account_name}' not found.")
            return None
        else:
            print(
                f"Failed to retrieve service accounts. Status code: {response.status_code}, Response: {response.text}"
            )
            return None

    def delete_service_account(self, service_account_id):
        """
        Delete an existing service account by its ID.

        :param service_account_id: ID of the service account to be deleted
        :return: True if deletion was successful, False otherwise
        """
        response = requests.delete(
            f"{self.grafana_url}/api/serviceaccounts/{service_account_id}",
            headers=self.headers,
            auth=self.auth,
        )
        if response.status_code == 200:
            print(f"Service Account with ID {service_account_id} deleted successfully.")
            return True
        else:
            print(
                f"Failed to delete service account. Status code: {response.status_code}, Response: {response.text}"
            )
            return False

    def delete_service_account_by_name(self):
        """
        Delete a service account by its name.

        :param name: Name of the service account to be deleted
        :return: True if deletion was successful, False otherwise
        """
        service_account_id = self.get_service_account_id_by_name()
        if service_account_id is None:
            return False

        response = requests.delete(
            f"{self.grafana_url}/api/serviceaccounts/{service_account_id}",
            headers=self.headers,
            auth=self.auth,
        )
        if response.status_code == 200:
            print(
                f"Service account '{self.service_account_name}' deleted successfully."
            )
            return True
        else:
            print(
                f"Failed to delete service account '{self.service_account_name}'. Status code: {response.status_code}, Response: {response.text}"
            )
            return False

    def get_key(self):
        self.auth = HTTPBasicAuth(self.admin_user, self.admin_password)
        self.headers = {"Content-Type": "application/json"}
        self.delete_service_account_by_name()

        service_account = self.create_service_account()

        if service_account:
            # Generate a token for the newly created service account
            token = self.generate_service_account_token(
                service_account_id=service_account["id"],
                token_name=self.service_account_token_name,
            )

            if token:
                print("Service Account Token Created")
                print(token)
