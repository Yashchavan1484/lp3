# Blockchain Technology (BT) - Group C

| Assignment | Title | File |
|---|---|---|
| C1 | Install MetaMask, study Ether spent per transaction | No code (practical on MetaMask) |
| C2 | Create your own wallet with MetaMask | No code (practical on MetaMask) |
| C3 | Bank account smart contract (deposit / withdraw / show balance) | `C3_BankAccount.sol` |
| C4 | Student data in Solidity (struct, array, fallback) + gas/fee | `C4_StudentData.sol` |
| C5 | Survey report on types of blockchains and use cases | No code (written report) |

## How to run C3 / C4 (Remix IDE - https://remix.ethereum.org)
1. Create a new file, paste the contract code.
2. Solidity Compiler tab -> compile (version 0.8.x).
3. Deploy & Run tab -> Environment: "Remix VM" (or "Injected Provider - MetaMask" on a test network like Sepolia).
4. **C3**: type a value in VALUE (e.g. 1 Ether), click `deposit`; call `showBalance`; call `withdraw` with an amount in wei.
5. **C4**: call `addStudent`, then `getStudent(0)` / `getStudentCount`. To trigger fallback, send a low-level
   transaction with random calldata (the "Low level interactions" box under the deployed contract).
6. For the gas / transaction fee observation, expand each transaction in the Remix console and note
   `gas`, `transaction cost`, and `execution cost`.
