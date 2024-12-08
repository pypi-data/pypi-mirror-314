from typing import Union, List, Dict
from dcentrapi.requests_dappi import requests_get, requests_post
from dcentrapi.Base import Base


class EventPolling(Base):
    def get_collection(self, collection_name: str):
        url = self.url + "event_polling/collection"
        data = {"collection_name": collection_name}
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def get_latest_contract_version(self, contract_name: str):
        url = self.url + "event_polling/get_latest_contract_version"
        data = {"contract_name": contract_name}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def register_user(self, user_name: str, collection_name: str):
        url = self.url + "event_polling/register_user"
        data = {
            "user_name": user_name,
            "collection_name": collection_name,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def subscribe_contract(
        self,
        contract_name: str,
        contract_address: str,
        network: str,
        abi: Union[str, List[Dict[str, str]]],
        collection_name: str,
        contract_version: str,
        git_tag: str = None,
        webhook_url: str = None,
    ):
        url = self.url + "event_polling/subscribe_contract"
        data = {
            "contract_name": contract_name,
            "contract_address": contract_address,
            "contract_version": contract_version,
            "network": network,
            "collection_name": collection_name,
            "abi": abi,
            "git_tag": git_tag,
            "webhook_url": webhook_url,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def get_schema(self, contract_name: str, contract_version: str):
        url = self.url + "event_polling/schema"
        data = {"contract_name": contract_name, "contract_version": contract_version}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_events_sum_of_values_in_range(
        self,
        collection_name: str,
        contract_address: str,
        event_name: str,
        field_name: str,
        start_time: str,
        end_time: str,
    ):
        url = self.url + "event_polling/events_sum_of_values_in_range"
        data = {
            "collection_name": collection_name,
            "contract_address": contract_address,
            "event_name": event_name,
            "field_name": field_name,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_contract_nof_transactions(self, collection_name: str, contract_address: str):
        url = self.url + "event_polling/contract_nof_transactions"
        data = {"collection_name": collection_name, "contract_address": contract_address}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_contract_users_in_time_range(
        self, collection_name: str, contract_address: str, start_time: str, end_time: str
    ):
        url = self.url + "event_polling/contract_users_in_time_range"
        data = {
            "collection_name": collection_name,
            "contract_address": contract_address,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_contracts_events_info(
        self,
        collection_name: str,
        contract_addresses: [str],
        event_names: [str],
        user_web3_addresses=None,
        start_time=None,
        end_time=None,
        incentive_id: str = None,
        user_address: str = None,
        sort: str = None,
    ):
        url = self.url + "event_polling/contracts_events_info"
        data = {
            "collection_name": collection_name,
            "contract_addresses": contract_addresses,
            "start_time": start_time,
            "end_time": end_time,
            "user_web3_addresses": user_web3_addresses,
            "event_names": event_names,
            "incentive_id": incentive_id,
            "user_address": user_address,
            "sort": sort,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def get_nof_contracts_events_unique_transactions(
        self, collection_name: str, contract_addresses: str, event_names: str
    ):
        url = self.url + "event_polling/contracts_events_info"
        data = {
            "collection_name": collection_name,
            "contract_addresses": contract_addresses,
            "event_names": event_names,
        }
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_nof_token_transfers(self, contract_addresses: [str]):
        url = self.url + "event_polling/token_transfers"
        data = {"contract_addresses": contract_addresses}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_event_details(self, collection_name: str, list_of_events: [str], event_parameter: str):
        url = self.url + "event_polling/get_event_details"
        data = {
            "collection_name": collection_name,
            "list_of_events": list_of_events,
            "event_parameter": event_parameter,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    # def get_collection_sum_of_values_in_range(
    #     self, collection_name: str, event_name: str, field_name: str, start_time: str, end_time: str
    # ):
    #     url = self.url + "event_polling/collection_sum_of_values_in_range"
    #     data = {
    #         "collection_name": collection_name,
    #         "event_name": event_name,
    #         "field_name": field_name,
    #         "start_time": start_time,
    #         "end_time": end_time,
    #     }
    #     response = requests_get(url=url, params=data, headers=self.headers)
    #     return response.json()

    def get_collection_contracts_sum_of_values(
        self, collection_name: str, event_name: str, field_name: str, start_time: str, end_time: str
    ):
        url = self.url + "event_polling/collection_contracts_sum_of_values"
        data = {
            "collection_name": collection_name,
            "event_name": event_name,
            "field_name": field_name,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_collection_daily_nof_transactions(self, collection_name: str, start_time: str, end_time: str):
        url = self.url + "event_polling/collection_daily_nof_transactions"
        data = {"collection_name": collection_name, "start_time": start_time, "end_time": end_time}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_collection_nof_transactions_by_time(self, collection_name, start_time, end_time):
        url = self.url + "event_polling/collection_nof_transactions_by_time"
        data = {"collection_name": collection_name, "start_time": start_time, "end_time": end_time}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_collection_nof_transactions(self, collection_name: str):
        url = self.url + "event_polling/collection_nof_transactions"
        data = {"collection_name": collection_name}
        response = requests_get(url=url, params=data, headers=self.headers)
        return response.json()

    def get_collection_nof_users_in_time_range(self, collection_name: str, start_time: str, end_time: str):
        url = self.url + "event_polling/collection_nof_users_in_time_range"
        data = {"collection_name": collection_name, "start_time": start_time, "end_time": end_time}
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()

    # def get_collection_users_in_time_range(self, collection_name: str, start_time: str, end_time: str):
    #     url = self.url + "event_polling/collection_users_in_time_range"
    #     data = {"collection_name": collection_name, "start_time": start_time, "end_time": end_time}
    #     response = requests_get(url=url, params=data, headers=self.headers)
    #     return response.json()
