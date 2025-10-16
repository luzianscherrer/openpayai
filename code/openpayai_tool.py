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


def generate_openpayai(directory: str, price: float, wallet: str):
    path = Path(directory).resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Not a valid directory: {directory}")

    random_uuid = uuid.uuid4().bytes
    digest = hashlib.sha256(random_uuid).hexdigest()
    token = f"0x{digest}"

    file_path = path / ".openpayai"
    file_path.write_text(token, encoding="utf-8")

    tx = contract.functions.addEntry(
        token, Web3.to_wei(price, "ether"), wallet
    ).build_transaction(
        {
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gas": 300000,
            "gasPrice": web3.eth.gas_price,
        }
    )
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Path: {file_path}")
    print(f"OpenPayAI identifier: {token}")
    print(f"Price: {price}")
    print(f"Data owner: {wallet}")
    print(f"Transaction {receipt.transactionHash.hex()}")


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
        generate_openpayai(args.directory, args.price, args.wallet)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
