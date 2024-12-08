# import traceback
# from dcentrapi.Base import Base, DapiError
# from dcentrapi.requests_dappi import requests_get
# from requests.exceptions import RequestException, HTTPError
# from json.decoder import JSONDecodeError
#
# # TODO: implmenent add_gas_fee_to_tx_payload which will enable dapi users to send a tx_payload + network chain id and
# #  have it filled with the proper gas fees
#
#
# class GasMonitor(Base):
#     def get_optimal_gas_price(self, network_name, minutes, stats=None, values=None):
#         url = self.url + "gas_monitor/optimal_gas_price_for_network"
#         data = {
#             "network_name": network_name,
#             "minutes": minutes,
#             "stats": stats,
#             "values": values,
#         }
#         response = None
#         try:
#             response = requests_get(url, params=data, headers=self.headers)
#             # Check response status code before attempting to parse JSON
#             response.raise_for_status()  # This will raise HTTPError for bad status codes
#             return response.json()  # Attempt to parse JSON
#         except JSONDecodeError as json_error:
#             # Handle JSON parsing errors specifically
#             error_message = f"Failed to parse JSON response: {json_error}"
#             raise DapiError(
#                 message=error_message,
#                 status_code=response.status_code if response is not None else None,
#                 response=response.text if response is not None else None,
#                 exception=json_error,
#             )
#         except HTTPError as http_error:
#             # Handle HTTP errors
#             error_message = f"HTTP error occurred: {http_error}"
#             raise DapiError(
#                 message=error_message,
#                 status_code=response.status_code if response is not None else None,
#                 response=response.text if response is not None else None,
#                 exception=http_error,
#             )
#         except RequestException as request_error:
#             # Handle other requests-related errors (e.g., network issues)
#             error_message = f"Request failed: {request_error}"
#             raise DapiError(
#                 message=error_message,
#                 status_code=response.status_code if response is not None else None,
#                 exception=request_error,
#             )
#         except Exception as e:
#             # Catch-all for any other exceptions
#             raise DapiError(
#                 message="An unexpected error occurred", exception=f"e: {e}, traceback: {traceback.format_exc()}"
#             )
