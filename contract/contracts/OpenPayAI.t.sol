// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

import {OpenPayAI} from "./OpenPayAI.sol";
import {Test} from "forge-std/Test.sol";

contract OpenPayAITest is Test {
    OpenPayAI openPayAI;

    function setUp() public {
        openPayAI = new OpenPayAI(
            msg.sender,
            0x6c3ea9036406852006290770BEdFcAbA0e23A0e8
        );
    }
}
