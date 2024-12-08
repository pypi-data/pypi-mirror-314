from typing import List
from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_post


# See: https://docs.tenderly.co/simulations-and-forks/intro-to-simulations
class TxSimulation(Base):

    # In functions below:
    # `sender` is the address that will sign the transaction(s)
    #     (This gets turned into a `from` attribute on the tx(s). Not using `from` directly because it is a Python reserved word.)
    # `tx` is a built transaction output from web3.py
    # `tx_bundle` is a list of built transactions output from web3.py

    # See: https://docs.tenderly.co/simulations-and-forks/simulation-api/using-simulation-api
    def simulate_transaction_single(
        self,
        sender: str,
        tx: dict,
    ):
        url = self.url + "simulateTransactions"
        data = {"sender": sender, "tx_single": tx}
        response = requests_post(url, json=data, headers=self.headers)
        return response.json()

    # Format of tx_bundle is [tx0, tx1, tx2...]
    # See: https://docs.tenderly.co/simulations-and-forks/simulation-api/simulation-bundles
    def simulate_transaction_bundle(
        self,
        sender: str,
        tx_bundle: List[dict],
    ):
        url = self.url + "simulateTransactions"
        data = {"sender": sender, "tx_bundle": tx_bundle}
        response = requests_post(url, json=data, headers=self.headers)
        return response.json()
