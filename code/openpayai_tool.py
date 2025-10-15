#!/usr/bin/env python3
import argparse
import hashlib
import uuid
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from web3 import Web3
from web3.exceptions import ContractLogicError
from eth_account import Account
from eth_account.messages import encode_defunct

load_dotenv()

RPC_URL = "http://localhost:8545"
PRIVATE_KEY = os.getenv("OPA_TOOL_PRIVATE_KEY")
ABI_PATH = "../contract/artifacts/contracts/OpenPayAI.sol/OpenPayAI.json"
ADR_PATH = "../contract/ignition/deployments/chain-31337/deployed_addresses.json"

with open(ABI_PATH, "r") as abi_file:
    contract_json = json.load(abi_file)
    CONTRACT_ABI = contract_json["abi"]

with open(ADR_PATH, "r") as addr_file:
    deployed = json.load(addr_file)
    CONTRACT_ADDRESS = deployed.get("OpenPayAIModule#OpenPayAI")

web3 = Web3(Web3.HTTPProvider(RPC_URL))
assert web3.is_connected(), "Failed to connect to Ethereum node"
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
account = web3.eth.account.from_key(PRIVATE_KEY)


def main():
    parser = argparse.ArgumentParser(
        description="Enable OpenPayAI for a given directory"
    )
    parser.add_argument("directory", help="Target directory to enable for OpenPayAI")
    parser.add_argument(
        "--price",
        type=float,
        required=True,
        help="Price to charge for access",
    )
    parser.add_argument(
        "--wallet", type=str, required=True, help="Wallet address to receive payments"
    )
    args = parser.parse_args()

    try:
        pass
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
