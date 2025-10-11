# OpenPayAI

## ETHOnline Hackathon

This project is my contribution to the [ETHOnline 2025 Hackathon](https://ethglobal.com/events/ethonline2025).

## Development Setup

### Directory Structure

- `contract/contracts`: Smart Contracts

### Used Software Versions

- Node 22.12.0
- NPX 10.9.0

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
