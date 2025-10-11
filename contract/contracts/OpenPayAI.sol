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

    constructor(address _owner) {
        owner = _owner;
    }

    modifier isOwner() {
        require(msg.sender == owner, "Not the Owner");
        _;
    }

    function withdraw() external isOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");

        (bool success, ) = payable(owner).call{value: balance}("");
        require(success, "Withdrawal failed");
    }

    receive() external payable {}
}
