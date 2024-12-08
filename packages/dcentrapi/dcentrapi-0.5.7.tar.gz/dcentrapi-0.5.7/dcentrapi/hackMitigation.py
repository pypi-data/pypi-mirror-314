import datetime
import logging
import traceback
from time import sleep
from dcentrapi.Base import Base, DapiError
from dcentrapi.requests_dappi import requests_get

logger = logging.getLogger()
logger.setLevel("INFO")


class HackMitigation(Base):
    def are_addresses_blacklisted(self, addresses: [str], check_malcon: bool = True, check_sanctioned: bool = False):
        url = self.url + "generic_freeze_signal/are_addresses_blacklisted"
        data = {
            "addresses": addresses,
            "check_malcon": check_malcon,
            "check_sanctioned": check_sanctioned,
        }
        response = None
        tries = 7
        while tries > 0:
            logger.info(f"{tries} more tries")
            before = datetime.datetime.now()
            logger.info(f"before request: {before}")
            try:
                response = requests_get(url, params=data, headers=self.headers)

                after = datetime.datetime.now()
                logger.info(f"after request: {after}")
                logger.info(f"time elapsed: {after-before}")

                if response.status_code == 200:
                    # Parse the JSON data using the json() method
                    response_data = response.json()
                    logger.info(f"data={response_data}")  # This will print the parsed JSON data as a Python dictionary
                    return response_data
                else:
                    msg = f"Request failed with status code: {response.status_code}"
                    if hasattr(response, "error_message"):
                        msg += f" and error message: {response.error_message}"
                    logger.error(msg)
                    tries -= 1
                    logger.info("sleeping for 1.75 secs")
                    sleep(1.75)

            except Exception as e:
                return DapiError(response=response.__dict__, exception=f"e: {e}, traceback: {traceback.format_exc()}")

        return DapiError(response=response.__dict__, exception="Stop retry after 7 tries")
