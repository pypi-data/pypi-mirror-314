import requests


class TransferData:
    def __init__(self, api_key: str) -> None:
        """
        Generate a trading data and transfer to Kafka with.

        Args:
            api_key (str): API key for authentication, used to connect to the Go API.
        """
        self.api_key = api_key

    def transfer_data(self) -> dict:
        """Calls the Go API to transfer trading data to Kafka."""
        headers = {"x-api-key": self.api_key}
        url = "http://go-api.blockhouse.app/transfer-data/send"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"error": str(e)}
