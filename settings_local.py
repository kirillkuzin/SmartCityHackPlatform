import os

APPLICATION_SETTINGS = {"PORT": os.getenv("PORT") or 5000}

ETHEREUM_SETTINGS = {
    "DEFAULT_GAS_PRICE": 21000000000,
    "DEFAULT_GAS": 1000000,
    "INFURA_LINK": os.getenv("INFURA_LINK"),
    "REGISTRY_CONTRACT_ADDRESS": \
        os.getenv("0x8135c49dbd537c59124c72e68730a9cc00c35c67"),
    "REGISTRY_CONTRACT_ABI": "abi/registry_contract_abi.json"
}

# DATABASE_SETTINGS = {
#     "DATABASE_URL": os.getenv("DATABASE_URL")
# }
