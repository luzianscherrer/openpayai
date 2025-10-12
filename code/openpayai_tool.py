#!/usr/bin/env python3
import json

ABI_PATH = "../contract/artifacts/contracts/OpenPayAI.sol/OpenPayAI.json"
ADR_PATH = "../contract/ignition/deployments/chain-31337/deployed_addresses.json"

with open(ABI_PATH, "r") as abi_file:
    contract_json = json.load(abi_file)
    CONTRACT_ABI = contract_json["abi"]

with open(ADR_PATH, "r") as addr_file:
    deployed = json.load(addr_file)
    CONTRACT_ADDRESS = deployed.get("OpenPayAIModule#OpenPayAI")

print(CONTRACT_ADDRESS)
