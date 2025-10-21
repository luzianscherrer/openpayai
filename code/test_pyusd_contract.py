from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
abi = [
    {
        "name": "name",
        "outputs": [{"type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "name": "symbol",
        "outputs": [{"type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "name": "decimals",
        "outputs": [{"type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
]
token = w3.eth.contract(address="0x6c3ea9036406852006290770BEdFcAbA0e23A0e8", abi=abi)
print(token.functions.name().call())
print(token.functions.symbol().call())
print(token.functions.decimals().call())
