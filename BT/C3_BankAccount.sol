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

This is a Solidity smart contract for a simple bank: users deposit ether, withdraw it, and check their balance. It is not an ML program, so instead of a model comparison I’ve compared safe vs unsafe withdraw patterns and call vs transfer vs send. Complexity is given in terms of gas, which is how smart contracts are measured.

Viva points to know before you go in:

owner is stored but never used anywhere. If asked, say it records the deployer and can be used for admin features later.
showBalance() returns the balance of whoever calls it (msg.sender), so each user only sees their own.
private does not hide data on the blockchain. It only blocks other contracts from reading it. Anyone can read the storage from the chain.
Aim

To create a smart contract on Ethereum (Solidity) that lets a user deposit ether, withdraw ether and view their balance.

Theory
A smart contract is a program stored on the blockchain that runs exactly as written, and its data and history cannot be changed.
Solidity is the language used for Ethereum smart contracts. pragma solidity ^0.8.0 means the compiler version is 0.8.0 or higher (below 0.9).
Ether and wei: 1 ether = 10¹⁸ wei. The contract works in wei, the smallest unit.
msg.sender is the address that called the function. msg.value is the amount of wei sent with the call.
payable means the function can receive ether.
mapping(address => uint256) is a key-value table that stores each user’s balance by address.
require(condition, "message") checks a condition. If it fails, the whole transaction is reverted (undone) with that message.
Events (emit) write logs to the blockchain, so apps and users can see what happened. indexed makes the address searchable.
view functions only read data, cost no gas when called directly, and do not create a transaction.
Checks-Effects-Interactions pattern: first check, then update the state, and only then send ether outside. The code does this in withdraw (the balance is reduced before the transfer), which prevents a reentrancy attack.
Overflow safety: from Solidity 0.8, arithmetic is checked automatically. Going below 0 or above the limit reverts the transaction.

Steps (how the contract works)
Deploy: the constructor runs once and saves the deployer as owner.
Deposit: the user sends ether with the call. The contract checks it is more than 0, adds it to the user’s balance and emits Deposited.
Withdraw: the contract checks the amount is more than 0 and not more than the balance, reduces the balance first, then sends the ether, checks that the send worked, and emits Withdrawn.
Show balance: returns the caller’s stored balance.

Tables to paste into GitHub

1. Function summary

markdown
| Function      | Type            | Input             | What it does                                   | Reverts when                                   |
|---------------|-----------------|-------------------|------------------------------------------------|------------------------------------------------|
| constructor   | Runs once       | None              | Saves deployer as `owner`                      | Never                                          |
| deposit()     | public payable  | ether via msg.value | Adds msg.value to caller's balance           | msg.value is 0                                 |
| withdraw(x)   | public          | amount in wei     | Reduces balance, sends ether to caller         | x is 0, balance is less than x, or send fails  |
| showBalance() | public view     | None              | Returns caller's balance                       | Never                                          |
| owner         | public variable| None              | Returns deployer's address                     | Never                                          |

2. Dry run in Remix (user A calls everything, 1 ether = 1000000000000000000 wei)

markdown
| Step | Action                          | Value sent (wei)        | Balance before | Balance after | Event emitted | Result                |
|------|---------------------------------|-------------------------|----------------|---------------|---------------|-----------------------|
| 1    | deposit()                       | 2000000000000000000 (2 ETH) | 0          | 2 ETH         | Deposited     | Success               |
| 2    | showBalance()                   | -                       | 2 ETH          | 2 ETH         | -             | Returns 2 ETH         |
| 3    | withdraw(500000000000000000)    | -                       | 2 ETH          | 1.5 ETH       | Withdrawn     | Success, 0.5 ETH sent |
| 4    | withdraw(5000000000000000000)   | -                       | 1.5 ETH        | 1.5 ETH       | -             | Reverts: "Insufficient balance" |
| 5    | deposit() with 0 value          | 0                       | 1.5 ETH        | 1.5 ETH       | -             | Reverts: "Deposit must be greater than 0" |

3. Key keywords

markdown
| Keyword / Term | Meaning                                                              |
|----------------|----------------------------------------------------------------------|
| msg.sender     | Address of the account calling the function                          |
| msg.value      | Amount of wei sent with the call                                     |
| payable        | Allows a function or address to receive ether                        |
| mapping        | Key-value storage, like a dictionary                                 |
| require        | Checks a condition, reverts the transaction if false                 |
| emit / event   | Writes a log entry on the blockchain                                 |
| view           | Reads data only, no state change, free when called directly          |
| uint256        | Unsigned 256-bit integer (no negative values)                        |
| wei            | Smallest ether unit, 1 ETH = 10^18 wei                               |
| gas            | Fee paid to run the code on the blockchain                           |

4. Complexity (Gas cost is the Solidity measure of time and space. n = number of users)

markdown
| Function      | Time (operations) | Approx. gas (varies)                  | Storage change                     | Reason                                          |
|---------------|-------------------|---------------------------------------|------------------------------------|-------------------------------------------------|
| deposit()     | O(1)              | About 21,000 base + 22,000 first deposit, about 5,000 later | One mapping entry, new or updated | One storage write, one event                    |
| withdraw()    | O(1)              | About 21,000 base + 5,000 write + 9,000 ether transfer | Updates one mapping entry | One read, one write, one external call          |
| showBalance() | O(1)              | 0 when called directly (view)         | None                               | One storage read                                |
| Whole contract| -                 | -                                     | O(n) space for n users             | One mapping entry per user who ever deposited   |

The gas numbers are approximate and depend on the network and on whether the storage slot is new. A mapping lookup is always O(1) (a hash of the key), no matter how many users exist. There are no loops, so the gas never grows with the number of users.

5. Safe vs unsafe withdraw

markdown
| Point                | Unsafe version (vulnerable)                    | This contract (safe)                            |
|----------------------|------------------------------------------------|-------------------------------------------------|
| Order of steps       | Send ether first, then reduce balance          | Reduce balance first, then send ether           |
| Reentrancy attack    | Possible (attacker re-enters before balance falls) | Not possible, balance is already reduced    |
| Pattern              | Violates Checks-Effects-Interactions           | Follows Checks-Effects-Interactions             |
| Famous example       | The 2016 DAO hack                              | Recommended practice                            |
| Extra protection     | None                                           | Can add a `nonReentrant` modifier as a second layer |

6. call vs transfer vs send

markdown
| Point                 | call (used here)                      | transfer                          | send                              |
|-----------------------|---------------------------------------|-----------------------------------|-----------------------------------|
| Gas forwarded         | All remaining gas                     | Fixed 2300 gas                    | Fixed 2300 gas                    |
| On failure            | Returns false, you must check it      | Reverts automatically             | Returns false, you must check it  |
| Works with contract wallets | Yes                             | May fail (2300 gas is too little) | May fail                          |
| Reentrancy risk       | Yes, unless state updated first       | Lower                             | Lower                             |
| Current recommendation| Recommended, with checks-effects-interactions | Discouraged now          | Discouraged                       |

7. Blockchain bank vs traditional bank

markdown
| Point                | Smart contract bank (this code)            | Traditional bank                         |
|----------------------|--------------------------------------------|------------------------------------------|
| Control              | Code, no middleman                         | Bank staff and central database          |
| Transparency         | All transactions are public                | Private                                  |
| Tampering            | Practically impossible to change records   | Possible by insiders                     |
| Availability         | 24/7                                       | Working hours or limited                 |
| Fees                 | Gas fees                                   | Service charges                          |
| Mistakes             | Cannot be reversed easily                  | Can be reversed or disputed              |
| Privacy              | Data visible on chain                      | Better                                   |
| Missing in this code | Interest, KYC, freeze, admin controls      | Available                                |
Why this design is good (and an honest note)
Safe withdraw order protects against reentrancy, the most famous smart contract attack.
Each user can only access their own balance, because everything is keyed by msg.sender.
require checks reject invalid inputs, and the whole transaction is undone if anything fails.
Events let front-end apps and auditors track every deposit and withdrawal cheaply.
No loops means the gas cost is constant and cannot be blown up by many users.
Honest limits for the viva: the contract has no transfer between users, no owner-only function, and no reentrancy guard. It also does not protect against ether forced in through selfdestruct, which is not counted in balances. The data is also not truly private, because private only affects Solidity access.
Easy example

Think of the contract as a locker room attendant who cannot be bribed.

Deposit: you hand over money, and the attendant writes your name and amount in a register that everyone can inspect.
Withdraw: you ask for some money back. The attendant first crosses out that amount from your line in the register, and only then hands you the cash. If he handed over cash first, you could shout “give me more” again before he updated the register, and that is exactly the reentrancy attack.
Show balance: you look only at your own line.
