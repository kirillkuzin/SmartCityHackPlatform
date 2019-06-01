import json

from web3 import Web3, HTTPProvider

from settings import ETHEREUM_SETTINGS

class Ethereum:
    web3 = Web3(HTTPProvider(ETHEREUM_SETTINGS["INFURA_LINK"]))

    def __init__(self, public_key=None, private_key=None):
        if public_key is not None:
            self.public_key = Web3.toChecksumAddress(public_key)
            self.private_key = private_key
        registry_contract_address = \
            ETHEREUM_SETTINGS["REGISTRY_CONTRACT_ADDRESS"]
        with open(ETHEREUM_SETTINGS["REGISTRY_CONTRACT_ABI"], "r") \
            as abi:
                registry_contract_abi = json.load(abi)
        self.registry_contract = self.web3.eth.contract(
            address = registry_contract_address,
            abi = registry_contract_abi
        )

    def build_tx(self):
        tx = self.registry_contract.buildTransaction({
            "gasPrice": ETHEREUM_SETTINGS["DEFAULT_GAS_PRICE"],
            "gas": ETHEREUM_SETTINGS["DEFAULT_GAS"],
            "nonce": self.__get_nonce()
        })
        return tx

    def send_eth_transaction(self, tx):
        signed = self.web3.eth.account.signTransaction(
            tx,
            private_key=self.private_key
        )
        tx_hash = \
            self.web3.eth.sendRawTransaction(signed.rawTransaction)
        return tx_hash

    def __get_nonce(self):
        return self.web3.eth.getTransactionCount(self.public_key)
