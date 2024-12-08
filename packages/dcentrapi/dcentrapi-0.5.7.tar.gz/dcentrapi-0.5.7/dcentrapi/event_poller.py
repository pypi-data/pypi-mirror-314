from typing import List, Dict, Optional, Union
from dcentrapi.requests_dappi import requests_post
from dcentrapi.Base import Base


class EventPoller(Base):
    def register_user(self, user_name: str, collection_name: str):
        url = self.url + "event_poller/user/register"
        data = {
            "user_name": user_name,
            "collection_name": collection_name,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def subscribe_contract(
        self,
        contract_address: str,
        contract_name: str,
        abi: List[dict],
        chain_id: str,
        deployment_block_number: int,
        subscribed_events: List[str],
        webhook_url: Optional[str] = None,
    ):
        url = self.url + "event_poller/contract/subscribe"
        data = {
            "contract_name": contract_name,
            "contract_address": contract_address,
            "abi": abi,
            "chain_id": chain_id,
            "deployment_block_number": deployment_block_number,
            "webhook_url": webhook_url,
            "subscribed_events": subscribed_events,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def update_contract(
        self,
        contract_address: str,
        chain_id: str,
        updated_name: Optional[str] = None,
        updated_abi: Optional[List[dict]] = None,
        updated_subscribed_events: Optional[List[str]] = None,
        updated_webhook_url: Optional[str] = None,
    ):
        url = self.url + "event_poller/contract/update"
        data = {
            "contract_address": contract_address,
            "chain_id": chain_id,
            "updated_name": updated_name,
            "updated_abi": updated_abi,
            "updated_subscribed_events": updated_subscribed_events,
            "updated_webhook_url": updated_webhook_url,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def get_contracts(
        self,
        chain_contract_map: Optional[Dict[str, Optional[Union[str, List[str]]]]] = None,
        page_size: Optional[int] = 500,
        page_number: Optional[int] = 1,
    ):
        url = self.url + "event_poller/contracts"
        data = {
            "chain_contract_map": chain_contract_map,
            "page_size": page_size,
            "page_number": page_number,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def deactivate_contracts(self, chain_contract_map: Dict[str, Optional[Union[str, List[str]]]]):
        url = self.url + "event_poller/contracts/deactivate"
        data = {
            "chain_contract_map": chain_contract_map,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def get_events(
        self,
        chain_contract_map: Optional[Dict[str, Optional[Union[str, List[str]]]]] = None,
        event_args: Optional[Dict[str, Optional[List[str]]]] = None,
        event_names: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        user_web3_addresses: Optional[List[str]] = None,
        block_number: Optional[int] = None,
        page_size: Optional[int] = 500,
        page_number: Optional[int] = 1,
    ):
        url = self.url + "event_poller/events"
        data = {
            "chain_contract_map": chain_contract_map,
            "event_args": event_args,
            "event_names": event_names,
            "start_time": start_time,
            "end_time": end_time,
            "user_web3_addresses": user_web3_addresses,
            "block_number": block_number,
            "page_size": page_size,
            "page_number": page_number,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()
