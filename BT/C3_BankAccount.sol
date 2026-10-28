// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Bank account smart contract: deposit, withdraw, show balance
contract BankAccount {
    address public owner;
    mapping(address => uint256) private balances;

    event Deposited(address indexed account, uint256 amount);
    event Withdrawn(address indexed account, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    // Deposit ether (send value along with the transaction)
    function deposit() public payable {
        require(msg.value > 0, "Deposit must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    // Withdraw `amount` (in wei) from the caller's balance
    function withdraw(uint256 amount) public {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount; // update state before transfer
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "Transfer failed");
        emit Withdrawn(msg.sender, amount);
    }

    // Show the caller's balance in the contract
    function showBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}
