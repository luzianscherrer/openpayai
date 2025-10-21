from web3 import Web3

RPC_URL = "http://localhost:8545"
PYUSD_ADDRESS = "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8"
ADDRESSES_TO_CHECK = [
    "0x8626f6940e2eb28930efb4cef49b2d1f2c9c1199",
    "0xDADAFAC167E4AEC1F40F71BBAC7949C9EE920F14",
]

web3 = Web3(Web3.HTTPProvider(RPC_URL))

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

pyusd = web3.eth.contract(
    address=Web3.to_checksum_address(PYUSD_ADDRESS), abi=ERC20_ABI
)

for address in ADDRESSES_TO_CHECK:
    target = Web3.to_checksum_address(address)
    balance = pyusd.functions.balanceOf(target).call()
    decimals = 6
    human_readable = balance / (10**decimals)
    print(f"Balance of {target}: {human_readable:>8.2f} PYUSD")
