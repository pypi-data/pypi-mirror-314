import pandas as pd
import requests
from loguru import logger


class BusinessCentralSession:
    """
    A session class for interacting with the Business Central API.
    """

    def __init__(self, username: str, password: str, base_url: str) -> None:
        """
        Initialize the session with authentication and base URL.
        :param username: API username.
        :param password: API password.
        :param base_url: Base URL of the Business Central API.
        """

        self.session = requests.Session()
        self.session.auth = (username, password)
        self.base_url = self._ensure_trailing_slash(base_url)
        self._verify_connection()

    @staticmethod
    def _ensure_trailing_slash(url: str) -> str:
        """Ensure the base URL ends with a trailing slash."""

        return url if url.endswith("/") else f"{url}/"

    def _verify_connection(self) -> None:
        """
        Verify the connection to the API and log the status.
        """

        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.info(f"Successfully connected to API at {self.base_url}")
        except requests.RequestException as e:
            logger.error(f"Failed to connect to {self.base_url}. Message: {str(e)}")
            raise ConnectionError(f"Failed to connect to {self.base_url}") from e

    def _build_query_url(self, service_name: str, filters: str = None, columns: list = None) -> str:
        """
        Build the query URL for the API endpoint.
        :param service_name: The name of the API service or endpoint.
        :param filters: OData filter string for query conditions.
        :param columns: List of column names to select.
        :return: Constructed query URL as a string.
        """

        query_params = []

        if filters:
            query_params.append(f"$filter={filters}")
        if columns:
            query_params.append(f"$select={','.join(columns)}")

        url = f"{self.base_url}{service_name}"
        query_string = "&".join(query_params)

        return f"{url}?{query_string}" if query_params else url

    def fetch_data(self, service_name: str, filters: str = "", columns: dict = None,
                   as_dataframe: bool = False) -> list | pd.DataFrame:
        """
        Fetch data from the Business Central API with optional filters and columns.

        :param service_name: The name of the service or endpoint.
        :param filters: OData filter string.
        :param columns: List of columns to select.
        :param as_dataframe: Return the result as a pandas DataFrame if True, else as a list.
        :return: List or DataFrame of fetched data.
        """

        selected_columns = list(columns.keys()) if columns else None
        url = self._build_query_url(service_name=service_name, filters=filters, columns=selected_columns)
        data = self._fetch_paginated_data(url)

        if as_dataframe:
            return self._convert_to_dataframe(data, columns=columns)

        return data

    def _fetch_paginated_data(self, url: str) -> list:
        """
        Fetch all data from paginated API responses.
        :param url: The initial query URL.
        :return: Combined list of all data records.
        """

        data = []

        while url:
            logger.debug(f"Fetching data from {url}")
            try:
                response = self.session.get(url)
                response.raise_for_status()
                json_response = response.json()
                data.extend(json_response.get("value", []))
                url = json_response.get("@odata.nextLink", None)
            except requests.RequestException as e:
                logger.error(f"Failed to fetch data from {url}. Message: {str(e)}")
                raise RuntimeError("Failed to fetch data from API") from e
        return data

    @staticmethod
    def _convert_to_dataframe(data: list, columns: dict = None) -> pd.DataFrame:
        """
        Convert the fetched data into a pandas DataFrame.
        :param data: List of data records.
        :param columns: Dictionary mapping API column names to desired column names.
        :return: Pandas DataFrame.
        """
        df = pd.DataFrame(data)

        if not df.empty:
            if "@odata.etag" in df.columns:
                df.drop(columns=["@odata.etag"], inplace=True)

            if not df.empty and columns:
                df.rename(columns=columns, inplace=True)  # Rename columns
                df = df[[val for val in columns.values() if val in df.columns]]  # Rearrange columns

        return df

    def __str__(self):
        """String representation of the session."""
        return f"BusinessCentralSession connected to {self.base_url}"
