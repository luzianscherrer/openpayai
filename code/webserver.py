from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from pathlib import Path
import base64
import json
import time
from web3 import Web3
from eth_account.messages import encode_defunct
from eth_account import Account

RPC_URL = "http://localhost:8545"
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

app = FastAPI()

WEBROOT = Path("../webroot").resolve()

app.mount("/", StaticFiles(directory=WEBROOT, html=True), name="static")


@app.middleware("http")
async def check_openpayai(request: Request, call_next):
    rel_path = request.url.path.lstrip("/") or "index.html"
    file_path = (WEBROOT / rel_path).resolve()

    if not str(file_path).startswith(str(WEBROOT)):
        return JSONResponse({"detail": "Forbidden"}, status_code=403)

    dir_path = WEBROOT / rel_path
    if dir_path.exists() and dir_path.is_dir() and not request.url.path.endswith("/"):
        return RedirectResponse(url=request.url.path + "/")

    if file_path.is_dir():
        file_path = file_path / "index.html"

    if file_path.exists():
        marker = file_path.parent / ".openpayai"
        if (
            marker.exists()
            and request.headers.get("user-agent", "") == "AI-Agent-Crawler"
        ):
            try:
                marker_content = marker.read_text(encoding="utf-8").strip()
            except Exception:
                marker_content = "unknown"

            verification_header = request.headers.get("X-OpenPayAI-Verification")
            if verification_header:
                print(f"Verification header: {verification_header}")
                try:
                    decoded_bytes = base64.b64decode(verification_header)
                    decoded_json = decoded_bytes.decode("utf-8")
                    data = json.loads(decoded_json)

                    address = data.get("address")
                    message = data.get("message")
                    signature = data.get("signature")

                    message_hash = encode_defunct(text=message)
                    recovered_address = Account.recover_message(
                        message_hash, signature=signature
                    )
                    signature_valid = recovered_address.lower() == address.lower()
                    if signature_valid:
                        print("Signature is valid")

                    timestamp_valid = False
                    identifier_valid = False
                    if message and "," in message:
                        ts_str, identifier = message.split(",", 1)
                        timestamp = int(ts_str)
                        now = int(time.time())
                        if abs(now - timestamp) <= 300:
                            timestamp_valid = True
                            print("Timestamp is valid")
                        if identifier == marker_content:
                            identifier_valid = True
                            print("Identifier is valid")

                    license_valid = contract.functions.licenses(
                        address, identifier
                    ).call()
                    if license_valid:
                        print("License is valid")

                    if (
                        signature_valid
                        and timestamp_valid
                        and license_valid
                        and identifier_valid
                    ):
                        return FileResponse(file_path)
                    else:
                        return JSONResponse(
                            {"detail": "X-OpenPayAI-Verification check failed"},
                            status_code=403,
                        )

                except Exception as e:
                    return JSONResponse(
                        {"detail": "X-OpenPayAI-Verification decoding failed"},
                        status_code=403,
                    )

            else:
                headers = {"X-OpenPayAI-Id": marker_content}
                return JSONResponse(
                    {"detail": "Payment Required"},
                    status_code=402,
                    headers=headers,
                )

    return await call_next(request)
