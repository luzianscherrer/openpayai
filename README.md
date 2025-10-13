# OpenPayAI

## ETHOnline Hackathon

This project is my contribution to the [ETHOnline 2025 Hackathon](https://ethglobal.com/events/ethonline2025).

### Used Sponsor Technology

- Nomic Foundation: [Hardhat 3](https://hardhat.org)
- Blockscout: [Autoscout](https://deploy.blockscout.com)

## Development Setup

### Directory Structure

| Directory            | Description     |
| -------------------- | --------------- |
| `contract/contracts` | Smart Contracts |
| `code`               | Tools           |

### Used Software Versions

- Node 22.12.0
- npx 10.9.0
- Python 3.13.2

### Python Setup

```
cd code
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Blockscout / ngrok Config

Use [ngrok](https://ngrok.com) to make the blockchain available to Blockscout's [Autoscout](https://deploy.blockscout.com). `ngrok config edit` to edit the config:

```
version: "3"
agent:
    authtoken: <token>
tunnels:
  blockchain:
    addr: 8545
    proto: http
    hostname: <subdomain>.ngrok-free.app
```

Then: `ngrok start --all`

## Demonstration

### Run the Blockchain

```
cd contract
npx hardhat node
```

### Deploy the Contract

```
cd contract
npx hardhat ignition deploy --network localhost ignition/modules/OpenPayAI.ts
```

### Run the Webserver

```
cd code
source venv/bin/activate
fastapi dev webserver.py
```

Then visit http://localhost:8000
