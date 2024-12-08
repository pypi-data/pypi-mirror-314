import traceback
from dcentrapi.Base import Base, DapiError
from dcentrapi.requests_dappi import requests_get
from requests.exceptions import RequestException, HTTPError
from json.decoder import JSONDecodeError


class GasFeeEstimator(Base):
    def get_gas_fee_estimation(self, chain_id: str, strategy: str = "market"):
        url = self.url + "gas_fee_estimator/get_gas_fee_estimation"
        data = {
            "chain_id": chain_id,
            "strategy": strategy,
        }

        response = None
        try:
            response = requests_get(url, params=data, headers=self.headers)
            # Check response status code before attempting to parse JSON
            response.raise_for_status()  # This will raise HTTPError for bad status codes
            return response.json()  # Attempt to parse JSON
        except JSONDecodeError as json_error:
            # Handle JSON parsing errors specifically
            error_message = f"Failed to parse JSON response: {json_error}"
            raise DapiError(
                message=error_message,
                status_code=response.status_code if response is not None else None,
                response=response.text if response is not None else None,
                exception=json_error,
            )
        except HTTPError as http_error:
            # Handle HTTP errors
            error_message = f"HTTP error occurred: {http_error}"
            raise DapiError(
                message=error_message,
                status_code=response.status_code if response is not None else None,
                response=response.text if response is not None else None,
                exception=http_error,
            )
        except RequestException as request_error:
            # Handle other requests-related errors (e.g., network issues)
            error_message = f"Request failed: {request_error}"
            raise DapiError(
                message=error_message,
                status_code=response.status_code if response is not None else None,
                exception=request_error,
            )
        except Exception as e:
            # Catch-all for any other exceptions
            raise DapiError(
                message="An unexpected error occurred", exception=f"e: {e}, traceback: {traceback.format_exc()}"
            )
