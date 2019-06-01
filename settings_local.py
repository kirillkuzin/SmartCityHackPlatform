import os

APPLICATION_SETTINGS = {"PORT": int(os.environ.get('PORT', 5000))}

ETHEREUM_SETTINGS = {
    "DEFAULT_GAS_PRICE": 21000000000,
    "DEFAULT_GAS": 1000000,
    "INFURA_LINK": os.getenv("INFURA_LINK"),
    "REGISTRY_CONTRACT_ADDRESS": os.getenv("REGISTRY_CONTRACT_ADDRESS"),
    "REGISTRY_CONTRACT_ABI": "abi/registry_contract_abi.json"
}

# DATABASE_SETTINGS = {
#     "DATABASE_URL": os.getenv("DATABASE_URL")
# }
