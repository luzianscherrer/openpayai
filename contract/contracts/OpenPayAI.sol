// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract OpenPayAI {
    struct Entry {
        uint256 price;
        address dataOwner;
    }
    address public immutable owner;
    mapping(bytes32 => Entry) public entries;
    mapping(address => mapping(bytes32 => bool)) public licenses;

    event EntryAdded(bytes32 indexed hash, uint256 price, address dataOwner);
    event PriceUpdated(bytes32 indexed hash, uint256 newPrice);
    event LicenseBought(address indexed buyer, bytes32 indexed hash);
    event Withdrawal(address indexed owner, uint256 amount);

    constructor(address _owner) {
        owner = _owner;
    }

    modifier isOwner() {
        require(msg.sender == owner, "Not the Owner");
        _;
    }
    modifier isDataOwner(bytes32 hash) {
        require(entries[hash].dataOwner == msg.sender, "Not the data owner");
        _;
    }

    function addEntry(
        bytes32 hash,
        uint256 price,
        address dataOwner
    ) external isOwner {
        require(entries[hash].dataOwner == address(0), "Entry already exists");

        entries[hash] = Entry({price: price, dataOwner: dataOwner});

        emit EntryAdded(hash, price, dataOwner);
    }

    function getEntry(bytes32 hash) external view returns (uint256, address) {
        require(entries[hash].dataOwner != address(0), "Entry does not exist");

        Entry memory entry = entries[hash];
        return (entry.price, entry.dataOwner);
    }

    function buyLicense(bytes32 hash) external payable {
        require(entries[hash].dataOwner != address(0), "Entry does not exist");
        require(msg.value >= entries[hash].price, "Insufficient funds");

        address dataOwner = entries[hash].dataOwner;
        uint256 price = entries[hash].price;

        (bool success, ) = dataOwner.call{value: price}("");
        require(success, "Transfer failed");

        licenses[msg.sender][hash] = true;

        emit LicenseBought(msg.sender, hash);
    }

    function updatePrice(
        bytes32 hash,
        uint256 newPrice
    ) external isDataOwner(hash) {
        require(entries[hash].dataOwner != address(0), "Entry does not exist");

        entries[hash].price = newPrice;

        emit PriceUpdated(hash, newPrice);
    }

    function withdraw() external isOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");

        (bool success, ) = payable(owner).call{value: balance}("");
        require(success, "Withdrawal failed");

        emit Withdrawal(owner, balance);
    }

    receive() external payable {}
}
