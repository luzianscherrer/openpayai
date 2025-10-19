# OpenPayAI

## Introduction

Content providers face a growing dilemma: they want their websites to remain open and discoverable by traditional search crawlers, yet they don’t want to give away their content for free to AI crawlers that scrape data for training and retrieval-augmented generation purposes.

In July 2025, Cloudflare introduced a [pay-per-crawl](https://blog.cloudflare.com/introducing-pay-per-crawl/) model, allowing **content providers to charge AI crawlers** via micropayments while keeping access open for other uses. However, their payment solution is centralized and monopolistic.

**OpenPayAI** is a proof of concept that takes this idea further by creating a decentralized alternative. Payments for access are handled transparently on a public blockchain, making the system **trustless, open, and permissionless** — anyone can participate without relying on a single gatekeeper.

## ETHOnline Hackathon

This project is my contribution to the [ETHOnline 2025 Hackathon](https://ethglobal.com/events/ethonline2025).

### Used Sponsor Technology

- Nomic Foundation: [Hardhat 3](https://hardhat.org)
- Blockscout: [Autoscout](https://deploy.blockscout.com)

## Technical Description

A directory on the content providing webserver can be enabled for OpenPayAI using `openpayai_tool.py`:

```
usage: openpayai_tool.py [-h] --price PRICE --wallet WALLET directory

Enable OpenPayAI for a given directory

positional arguments:
  directory        Target directory to enable for OpenPayAI

options:
  -h, --help       show this help message and exit
  --price PRICE    Price to charge for access
  --wallet WALLET  Wallet address to receive payments
```

This writes a unique identifier to the directory on the webserver in a file
called `.openpayai`. The same identifier is stored together with the price and
the content owner's wallet address in the OpenPayAI smart contract on-chain.

Clients detected as being AI crawlers by their `User-Agent` header are not
allowed free access to such OpenPayAI enabled content. They get a HTTP 402 (Payment
Required) status and a header `X-OpenPayAI-Id` returned.

```
$ curl -I -H "User-Agent: AI-Agent-Crawler" http://localhost:8000/crane/
HTTP/1.1 402 Payment Required
date: Fri, 17 Oct 2025 15:01:12 GMT
x-openpayai-id: 0x76f3e01aff36f7ea119c74ff2687fae778c1aeb1709227857ecdf7884d66b3e1
```

Using this identifier, the crawlers can then lookup the price for accessing the
content in the OpenPayAI smart contract and submit a purchase transaction.

Once the purchase transaction is completed, the crawlers can request access to
the now licensed content again, but this time using a `X-OpenPayAI-Verification`
header. This header contains the base64 encocerd message
"`<timestamp>,<identifier>`" along with a cryptographic signature.

```
{
   "address" : "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
   "message" : "1755517272,0x76f3e01aff36f7ea119c74ff2687fae778c1aeb1709227857ec[...]",
   "signature" : "748d04eeadbf77cef5b4ee205a95e32e4bf249e20bb264b075d04dfd349fca[...]"
}
```

The content
providing webserver verifies that all of the following critera are met:

- The signature is valid
- The signer has purchased a license on-chain
- The identifier in the signed message is equal to the identifier of the requested OpenPayAI enabled content
- The timestamp is within 5 minutes of the current time (in order to prevent replay misuse)

If all checks are valid, the licensed content is returned to the crawler.

Ensured by the OpenPayAI smart contract, the content owner's wallet was already
automatically credited with the set price when the crawler did execute the
purchase transaction on-chain.

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
