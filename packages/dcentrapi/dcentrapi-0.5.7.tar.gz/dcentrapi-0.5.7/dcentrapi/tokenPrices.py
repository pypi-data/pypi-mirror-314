from typing import List
from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_get


class TokenPrices(Base):

    def get_token_prices_by_network_name_and_address(self, network_names: List[str], token_addresses: List[str]):
        url = self.w3i_url + "tokenPricesByNetworkAndAddress"
        data = {
            "network_names": network_names,
            "token_addresses": token_addresses,
        }
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()

    def get_token_prices_by_chain_id_and_address(self, chain_ids: List[str], token_addresses: List[str]):
        url = self.w3i_url + "tokenPricesByNetworkAndAddress"
        data = {
            "chain_ids": chain_ids,
            "token_addresses": token_addresses,
        }
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()
