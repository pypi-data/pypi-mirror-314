from .client import APIClient

class QueryAPI:
    def __init__(self, client: APIClient):
        """
        Initialize Query API.
        :param client: Instance of APIClient.
        """
        self.client = client

    def import_csv(self, csv_file_path: str, token: str):
        """
        Import student data from a CSV file.
        :param csv_file_path: Path to the CSV file.
        :param token: Authentication token for API call.
        :return: API response.
        """
        with open(csv_file_path, "rb") as file:
            files = {"file": file}
            data = {"token": token}
            return self.client.request("POST", "/api/import-csv", files=files, data=data)

    def download_csv(self, file_name: str, output_path: str):
        """
        Download processed CSV files (duplicates or errors).
        :param file_name: Name of the file to download.
        :param output_path: Path to save the downloaded file.
        :return: Path to the saved file.
        """
        response = self.client.request("GET", f"/api/download-csv/{file_name}", stream=True)
        with open(output_path, "wb") as file:
            file.write(response.content)
        return output_path
