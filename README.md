# OpenPayAI

## ETHOnline Hackathon

This project is my contribution to the [ETHOnline 2025 Hackathon](https://ethglobal.com/events/ethonline2025).

### Used Sponsor Technology

- Nomic Foundation: [Hardhat 3](https://hardhat.org)
- Blockscout: [Autoscout](https://deploy.blockscout.com)

## Development Setup

### Directory Structure

| Directory            | Description              |
| -------------------- | ------------------------ |
| `contract/contracts` | Smart Contracts          |
| `code`               | Tools                    |
| `webroot`            | Webserver Root Directory |

### Used Software Versions

- Node 22.12.0
- npx 10.9.0
- Python 3.13.2

### Node Setup

```
cd contract
npm install
```

### Python Setup

```
cd code
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` to set:

- `OPA_TOOL_PRIVATE_KEY`
- `AI_AGENT_PRIVATE_KEY`
- `OPENAI_KEY`.

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

### Run the AI Agent

```
cd code
source venv/bin/activate
python ai_agent.py
```

### Ask AI Agent for Summary

Prompt:

```
Please summarize the story on the website http://localhost:8000/cat in one sentence
```

### Enable OpenPayAI for an URL

```
cd code
source venv/bin/activate
./openpayai_tool.py --price 0.01 --wallet 0xdAdaFaC167E4aEC1F40F71BBac7949c9Ee920F14 ../webroot/crane/
```

### Verify OpenPayAI protection

```
curl -I -H "User-Agent: AI-Agent-Crawler" http://localhost:8000/crane/
```

### Ask AI Agent for Summary of OpenPayAI-enabled URL

Prompt:

```
Please summarize the story on the website http://localhost:8000/crane in one sentence
```

## Other Useful Commands

### Observe All Traffic

```
sudo tcpdump -i any -s 0 -A 'tcp port 8000'
```
