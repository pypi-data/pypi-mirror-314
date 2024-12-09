import requests
import pandas as pd

from api_to_dataframe.utils.logger import log, LogLevel


class GetData:
    @staticmethod
    def get_response(endpoint: str, headers: dict, connection_timeout: int):
        response = requests.get(endpoint, timeout=connection_timeout, headers=headers)
        response.raise_for_status()
        return response

    @staticmethod
    def to_dataframe(response):
        try:
            df = pd.DataFrame(response)
        except Exception as err:
            log(f"Error serializing to dataframe: {err}", LogLevel.ERROR)
            raise TypeError(
                f"Invalid response for transform in dataframe: {err}"
            ) from err

        if df.empty:
            log("DataFrame is empty", LogLevel.ERROR)
            raise ValueError("::: DataFrame is empty :::")

        return df
