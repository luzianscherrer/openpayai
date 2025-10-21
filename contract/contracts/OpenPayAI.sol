// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract OpenPayAI {
    struct Entry {
        uint256 price;
        address dataOwner;
    }
    address public immutable owner;
    IERC20 public immutable paymentToken;
    mapping(bytes32 => Entry) public entries;
    mapping(address => mapping(bytes32 => bool)) public licenses;

    event EntryAdded(bytes32 indexed hash, uint256 price, address dataOwner);
    event PriceUpdated(bytes32 indexed hash, uint256 newPrice);
    event LicenseBought(
        address indexed buyer,
        bytes32 indexed hash,
        uint256 price
    );
    event Withdrawal(address indexed owner, uint256 amount);

    constructor(address _owner, address _paymentToken) {
        owner = _owner;
        paymentToken = IERC20(_paymentToken);
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

        Entry memory entry = entries[hash];
        uint256 price = entry.price;
        address dataOwner = entry.dataOwner;

        bool success = paymentToken.transferFrom(msg.sender, dataOwner, price);
        require(success, "Token transfer failed");

        licenses[msg.sender][hash] = true;

        emit LicenseBought(msg.sender, hash, price);
    }

    function updatePrice(
        bytes32 hash,
        uint256 newPrice
    ) external isDataOwner(hash) {
        require(entries[hash].dataOwner != address(0), "Entry does not exist");

        entries[hash].price = newPrice;

        emit PriceUpdated(hash, newPrice);
    }

    function withdraw(uint256 amount) external isOwner {
        bool success = paymentToken.transfer(owner, amount);
        require(success, "Withdrawal failed");

        emit Withdrawal(owner, amount);
    }

    receive() external payable {}
}
