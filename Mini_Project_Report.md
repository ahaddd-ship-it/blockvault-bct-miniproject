# BLOCKVAULT: A DECENTRALIZED CORE BANKING LEDGER WITH SMART CONTRACT INTEGRATION

**Mini-Project Report for Blockchain Lab**  
*Submitted in partial fulfillment of the requirements of the Mini-Project of Blockchain Lab for Fourth Year of Bachelors of Engineering*

**Department of Artificial Intelligence & Data Science Engineering**  
**Rizvi College of Engineering, University of Mumbai (2026-2027)**

---

## CERTIFICATE
This is to certify that the mini-project entitled **“BlockVault: A Decentralized Core Banking Ledger with Smart Contract Integration”** is a bonafide work of the student(s) submitted to the University of Mumbai in partial fulfillment of the requirement for the Mini-Project of Blockchain Lab for Fourth Year of the Bachelor of Engineering in *Artificial Intelligence & Data Science*.

Guide / Prof. In-Charge: ____________________  
Head of Department: _______________________  
Principal, RCOE: Dr. Varsha Shah  

---

## DECLARATION
I declare that this written submission represents my ideas in my own words and where others' ideas or words have been included, I have adequately cited and referenced the original sources. I also declare that I have adhered to all principles of academic honesty and integrity and have not misrepresented or fabricated or falsified any idea/data/fact/source in my submission.

---

## ABSTRACT
Traditional centralized banking architectures suffer from single points of failure, opacity in interbank settlements, vulnerability to malicious insider database alterations, and high reconciliation overheads. This project, **BlockVault**, presents a decentralized core banking ledger prototype leveraging cryptographic hashing, immutable linked data structures, and automated smart contracts. 

BlockVault implements a distributed ledger powered by the SHA-256 algorithm and Proof-of-Work (PoW) consensus. Each block cryptographically seals transactions via a binary Merkle tree root, guaranteeing $O(\log n)$ tamper detection and lightweight proof of inclusion. In addition to peer-to-peer fund transfers, the platform incorporates programmatic smart contracts governing overdraft protection, interest-yielding term deposits, and collateralized micro-loans under strict loan-to-value (LTV) constraints. A visual dashboard provides interactive transaction broadcasting, block mining, and real-time ledger inspection. Furthermore, an attack simulation module allows intentional ledger tampering to empirically demonstrate the avalanche effect and the mathematical resilience of blockchain immutability.

---

## INDEX
1. **Introduction**
2. **System Analysis**
3. **System Design**
4. **Technologies Used**
5. **Implementation**
6. **Output Screenshots & Flow**
7. **Testing**
8. **Results and Discussions**
9. **Conclusion & Future Scope**
10. **References**
11. **Appendix**

---

## 1. INTRODUCTION

### 1.1 Background
Conventional banking systems depend on centralized database architectures (e.g., Relational Database Management Systems managed by central administrators). While performant, centralized ledgers introduce distinct systemic risks:
- Vulnerability to unauthorized database modifications (insider threats or cyber attacks).
- Requirement of trusted central intermediaries for auditing and inter-bank clearing.
- Disconnected silos requiring manual, expensive reconciliation processes.

### 1.2 Motivation
Blockchain and distributed ledger technology (DLT) provide a paradigm shift by transitioning from "trust through authority" to "trust through cryptographic verification". By combining public-key cryptography, linked list hashing, and consensus protocols, blockchain enables mutually untrusted parties to maintain a single, synchronized, and tamper-resistant truth.

### 1.3 Problem Statement
To design and build an educational yet functional decentralized core banking prototype (**BlockVault**) that models peer-to-peer banking settlements, demonstrates the cryptographic integrity of blockchain blocks, enforces autonomous smart contract banking rules, and offers visual proof of immutability against malicious data tampering.

### 1.4 Objectives
1. Implement a blockchain ledger from first principles featuring SHA-256 block hashing and previous hash pointer chaining.
2. Formulate a Proof-of-Work (PoW) consensus mechanism that dynamically evaluates block nonces against target difficulty.
3. Construct binary Merkle trees for each block to ensure mathematical transaction integrity.
4. Program smart contract logic for core banking actions: overdraft prevention, term deposits/staking, and collateralized micro-lending.
5. Create an interactive dashboard with attack simulation to validate tamper-resistance.

---

## 2. SYSTEM ANALYSIS

### 2.1 Existing System vs. Proposed System

| Feature | Existing Centralized Banking Ledger | Proposed BlockVault Decentralized Ledger |
| :--- | :--- | :--- |
| **Data Storage** | Centralized Relational SQL DB | Cryptographically linked block ledger |
| **Trust Model** | Trust placed in central bank admin | Algorithmic trust via cryptography |
| **Tamper Resistance** | Vulnerable to direct SQL modification | Mathematically irreversible via SHA-256 links |
| **Auditability** | Opaque, requires external auditor | Transparent, verifiable by every node |
| **Smart Automation** | Batch backend jobs prone to latency | Automated smart contracts executed on ledger |
| **Single Point of Failure** | Present at database server level | Distributed consensus protocol |

### 2.2 Functional Requirements
- **FR-1**: User Account Management with balance query audited from full ledger history.
- **FR-2**: Transaction Creation & Mempool broadcast for peer-to-peer transfers.
- **FR-3**: Block Mining with configurable Proof-of-Work difficulty and miner rewards.
- **FR-4**: Merkle Root computation for all transactions bundled in a block.
- **FR-5**: Smart Contract Execution:
  - *Overdraft Guard*: Reject any transfer exceeding available balance.
  - *Term Staking*: Lock funds for fixed months with deterministic yield.
  - *Micro-Lending*: Collateral-based lending requiring maximum 70% Loan-to-Value (LTV).
- **FR-6**: Cryptographic Chain Verification verifying all hashes, links, and Merkle roots.
- **FR-7**: Tamper Simulation allowing modification of historic block data to prove instant anomaly detection.

### 2.3 Non-Functional Requirements
- **Security & Integrity**: 100% cryptographic detection of any byte altered in historical blocks.
- **Performance**: Sub-second local Proof-of-Work execution for difficulty $d=2$ with deterministic memory utilization.
- **Usability**: Interactive web dashboard with real-time state feedback and visual block chain links.

---

## 3. SYSTEM DESIGN

### 3.1 Architectural Diagram (Mermaid)

```
+-----------------------------------------------------------+
|                    Client Web Dashboard                   |
|  - Account Balances   - Transaction Form   - Mining Tool  |
|  - Smart Contracts    - Chain Viewer       - Attack Lab   |
+-----------------------------+-----------------------------+
                              | REST / HTTP API
                              v
+-----------------------------------------------------------+
|                     FastAPI Backend Engine                |
|  - Endpoints: /api/transaction, /api/mine, /api/state     |
|  - Smart Contract API Router & Error Handlers             |
+-----------------------------+-----------------------------+
                              |
               +--------------+--------------+
               v                             v
+-----------------------------+ +---------------------------+
|    Smart Contract Engine    | |    Blockchain Core Ledger  |
|  - Overdraft Verifier       | |  - Blocks & Block Headers |
|  - Term Deposit Calculator  | |  - SHA-256 Hasher         |
|  - 70% LTV Micro-Loan Guard | |  - Merkle Tree Generator  |
+-----------------------------+ |  - PoW Consensus Miner    |
                                |  - Mempool (Unconfirmed)  |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |  Persistent JSON Ledger   |
                                +---------------------------+
```

### 3.2 Block Data Structure
Each block in BlockVault contains:
- `index`: Monotonically increasing sequence number ($0, 1, 2, \dots$).
- `timestamp`: Epoch timestamp of block creation.
- `transactions`: List of serialized transactions included in the block.
- `merkle_root`: SHA-256 Merkle root summarizing the transaction set.
- `previous_hash`: SHA-256 hash of block $i - 1$.
- `nonce`: Integer adjusted during mining to achieve leading zero requirement.
- `hash`: Resulting SHA-256 hash of the block header.

### 3.3 Cryptographic Formulae
$$\text{Block Hash} = \text{SHA256}(\text{Index} \parallel \text{Merkle Root} \parallel \text{Prev Hash} \parallel \text{Nonce} \parallel \text{Timestamp})$$
$$\text{PoW Target Criterion}: \text{Block Hash} < 2^{256 - 4 \times \text{Difficulty}}$$

---

## 4. TECHNOLOGIES USED

1. **Python 3.11**: Primary language for blockchain logic, cryptography, and server-side processing.
2. **FastAPI**: Asynchronous web framework providing RESTful endpoints and request validation.
3. **Uvicorn**: Lightning-fast ASGI web server implementation.
4. **HTML5 / CSS3 / Bootstrap 5**: Responsive dark-mode dashboard interface with grid layout and visual badges.
5. **JavaScript (ES6+)**: Frontend reactive state polling and asynchronous AJAX calls.
6. **Hashlib (Standard Library)**: Cryptographic SHA-256 engine.
7. **Jinja2**: HTML templating engine.

---

## 5. IMPLEMENTATION DETAILS

### 5.1 Transaction Module (`transaction.py`)
Encapsulates sender, recipient, amount, transaction type (`TRANSFER`, `DEPOSIT`, `MINING_REWARD`, `STAKING_DEPOSIT`, `LOAN_DISBURSE`), and cryptographic transaction hash calculation.

### 5.2 Block & Merkle Tree Module (`block.py`)
Computes Merkle trees by iteratively hashing pairwise transaction hashes until a single 256-bit root remains. Houses the `mine_block()` method executing the Proof-of-Work loop.

### 5.3 Smart Contract Engine (`smart_contract.py`)
Implements business rules preventing negative balances and executing lending protocols based on mathematical constraints.

### 5.4 Blockchain Core (`blockchain.py`)
Maintains the linked block sequence, memory pool (mempool), account balance audit through total transaction reconstruction, block append validation, and the attack simulation module.

---

## 6. OUTPUT SCREENSHOTS & OPERATION WORKFLOW

### Step 1: Genesis Block & Reserve Initialization
On initial boot, the blockchain generates Block `#0` (Genesis Block) with an initial protocol reserve and credits starter demo accounts (Alice, Bob, Charlie).

### Step 2: Peer-to-Peer Transfer Execution
A user initiates a transfer from Alice to Bob for $250.00. The smart contract validates Alice's balance. The transaction is queued in the unconfirmed Mempool.

### Step 3: Block Mining via Proof-of-Work
The miner triggers mining. The PoW engine calculates nonces until a hash starting with two leading zeros (`00...`) is found. Block `#2` is sealed and appended to the ledger.

### Step 4: Smart Contract Staking & Micro-Loans
Users lock funds in term deposits or pledge collateral to receive instantaneous micro-loans up to 70% of the collateral value.

### Step 5: Attack & Tamper Demonstration
When an attacker modifies historical Block `#1` transaction data, the dashboard status turns bright red:
`SECURITY ALERT: Broken Chain / Tampered Data: Merkle root invalid!`
This visual feedback demonstrates the immutability property of blockchain.

---

## 7. TESTING

### Test Cases & Validation Matrix

| Test ID | Test Scenario | Input / Action | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Genesis Block Creation | Server startup | Chain initialized with Block #0 | Block #0 generated with 64 zeros previous hash | **PASS** |
| **TC-02** | Valid Transaction | Alice sends $100 to Bob | Tx enters mempool | Mempool count increments to 1 | **PASS** |
| **TC-03** | Overdraft Protection | Charlie attempts to transfer $9999 | Tx rejected by smart contract | HTTP 400 Insufficient funds error returned | **PASS** |
| **TC-04** | Proof-of-Work Consensus | Click 'Mine Block' | Valid nonce found, hash starts with '00' | Block mined, hash validated, miner rewarded | **PASS** |
| **TC-05** | Merkle Root Integrity | Verify block transactions | Altering 1 transaction alters root | Merkle root changes completely | **PASS** |
| **TC-06** | Tamper Detection | Hack Block #1 Tx amount to $999999 | Blockchain flags invalid state | Chain integrity alert turns red with exact error | **PASS** |
| **TC-07** | Consensus Recovery | Click 'Restore Consensus' | Reload clean ledger state | Ledger integrity restored to 100% verified | **PASS** |

---

## 8. RESULTS AND DISCUSSIONS

The implementation of BlockVault demonstrates several core principles of blockchain technology:
1. **Mathematical Tamper-Evidence**: Changing even one cent ($0.01) in a past transaction completely invalidates the Merkle root and breaks the cryptographic hash pointer of all succeeding blocks.
2. **Elimination of Reconciliation**: Every node maintains an identical, auditable sequence of transactions, removing the need for batch ledger reconciliation.
3. **Autonomous Execution**: Smart contracts execute automatically without human intervention, rejecting invalid transactions deterministically.

---

## 9. CONCLUSION & FUTURE SCOPE

### Conclusion
BlockVault successfully demonstrates the application of blockchain and smart contracts in core banking. By implementing SHA-256 block linking, Proof-of-Work mining, Merkle tree transaction proofs, and an interactive banking interface, the project provides a comprehensive practical demonstration of Blockchain and Technology principles.

### Future Scope
- Transition from Proof-of-Work to Proof-of-Stake (PoS) to minimize energy consumption.
- Integration of Zero-Knowledge Proofs (zk-SNARKs) for balance privacy while preserving verifiability.
- Peer-to-peer WebSocket synchronization across multiple physical distributed nodes.

---

## 10. REFERENCES
1. Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System*.
2. Antonopoulos, A. M. (2017). *Mastering Bitcoin: Programming the Open Blockchain*. O'Reilly Media.
3. Wood, G. (2014). *Ethereum: A Secure Decentralised Generalised Transaction Ledger*. Ethereum Project Yellow Paper.
4. Tapscott, D., & Tapscott, A. (2016). *Blockchain Revolution: How the Technology Behind Bitcoin Is Changing Money, Business, and the World*. Penguin.

---

## 11. APPENDIX
- **Programming Language**: Python 3.11.9
- **Framework**: FastAPI 0.141.1, Uvicorn 0.52.4
- **Source Code Repository**: Local directory `C:\ai-agent-automations\mini project bct`
- **Dashboard URL**: `http://127.0.0.1:8000`
