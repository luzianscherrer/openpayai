from smolagents import ToolCallingAgent, tool, OpenAIServerModel
from dotenv import load_dotenv
import os
import requests
from web3 import Web3
from web3.exceptions import ContractLogicError
from eth_account.messages import encode_defunct
import json
import time
import base64

load_dotenv()

RPC_URL = "http://localhost:8545"
PRIVATE_KEY = os.getenv("AI_AGENT_PRIVATE_KEY")
ABI_PATH = "../contract/artifacts/contracts/OpenPayAI.sol/OpenPayAI.json"
ADR_PATH = "../contract/ignition/deployments/chain-31337/deployed_addresses.json"
OPENAI_KEY = os.environ["OPENAI_KEY"]

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


@tool
def retrieve_website_after_payment(url: str, identifier: str) -> str:
    """
    Retrieve the content of a website that a OpenPayAI payment has been made for.

    Args:
        url: The URL of the website to retrieve.
        identifier: OpenPayAI identifier.

    Returns:
        The raw text content of the website if accessible.
    """
    plain_message = f"{int(time.time())},{identifier}"
    encoded_message = encode_defunct(text=plain_message)
    signed_message = web3.eth.account.sign_message(encoded_message, PRIVATE_KEY)
    data = {
        "address": account.address,
        "message": plain_message,
        "signature": signed_message.signature.hex(),
    }
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    response = requests.get(
        url,
        headers={
            "X-OpenPayAI-Verification": encoded_data,
            "User-Agent": "AI-Agent-Crawler",
        },
    )
    response.raise_for_status()
    return response.text


@tool
def buy_access_to_website(identifier: str) -> str:
    """
    Buy access to website content based on a OpenPayAI identifier.

    Args:
        identifier: The OpenPayAI identifier of the website.

    Returns:
        A confirmation once payment is settled.
    """
    entry = contract.functions.entries(identifier).call()
    price = entry[0]
    tx = contract.functions.buyLicense(identifier).build_transaction(
        {
            "from": account.address,
            "value": price,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gas": 200000,
            "gasPrice": web3.eth.gas_price,
        }
    )
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        gas_used = receipt["gasUsed"]
        print(
            f"Bought OpenPayAI license for {Web3.from_wei(price, 'ether')} with transaction 0x{receipt.transactionHash.hex()} (used gas: {gas_used})"
        )
    except ContractLogicError as e:
        print(f"Transaction failed: {e}")
    return f"You can now retrieve the website content using the retrieve_website_after_payment tool with the OpenPayAI identifier {identifier}."


@tool
def retrieve_website(url: str) -> str:
    """
    Retrieve the content of a website.

    Args:
        url: The URL of the website to retrieve.

    Returns:
        The raw text content of the website if accessible.
        If the content requires payment for access, the
        OpenPayAI identifier is returned.
    """
    response = requests.get(url, headers={"User-Agent": "AI-Agent-Crawler"})

    if response.status_code == 402:
        pay_id = response.headers.get("X-OpenPayAI-Id")
        if pay_id:
            return f"OpenPayAI identifier: {pay_id}"
        else:
            return "OpenPayAI identifier: unknown"

    response.raise_for_status()
    return response.text


model = OpenAIServerModel(model_id="gpt-4o", api_key=OPENAI_KEY)
agent = ToolCallingAgent(
    tools=[retrieve_website, buy_access_to_website, retrieve_website_after_payment],
    model=model,
)

agent.prompt_templates["system_prompt"] = agent.prompt_templates["system_prompt"] + "\n"


while True:
    query = input("Prompt: ")
    if query.lower() in ["quit", "q", "exit"]:
        print("Goodbye!")
        break
    agent.run(query, reset=False)
