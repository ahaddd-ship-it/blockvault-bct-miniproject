# BlockVault: Decentralized Core Banking Ledger Prototype
**Subject**: Blockchain and Technology (BCT) — Mini Project  
**Department**: Artificial Intelligence & Data Science Engineering  

---

## 📌 1. Project Overview & Architecture

**BlockVault** is an end-to-end, full-stack decentralized banking prototype designed to illustrate the core mechanics of blockchain technology within financial systems:
- **Immutable Ledger**: Cryptographic linkage of blocks through **SHA-256** hash pointers.
- **Proof-of-Work (PoW) Consensus**: Mining engine adjusting cryptographic nonces to meet target difficulty.
- **Merkle Tree Integrity**: Automatic calculation of binary Merkle root trees for all transactions in every block.
- **Smart Contracts Engine**: Automated banking business logic including:
  1. *Account Overdraft Prevention* (Validation rules)
  2. *Automated Term Deposits / Staking* (7% APY locked yields)
  3. *Collateralized Micro-Lending* (70% Max Loan-to-Value auto-approval & disbursement)
- **Live Interactive Attack / Tamper Simulator**: Allows live demonstration of blockchain's self-verifying security when an attacker attempts to alter transaction history in past blocks.
- **Consensus Restoration**: Instant repair and sync with the consensus state.

---

## 🚀 2. How to Run the Project

### Prerequisites
- Python 3.10+ (Installed on system)

### Run the Web Server
Open a terminal in `C:\ai-agent-automations\mini project bct` and run:

```powershell
python app.py
```

Or with `uvicorn`:
```powershell
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### Access the Web Dashboard
Open your browser and visit:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🛠️ 3. Key Features Demonstrated in UI

1. **Live Ledger Explorer**:
   - Inspect Block `#0` (Genesis Block), Block `#1`, etc.
   - View Block Hash, Previous Hash link, Merkle Root, Nonce, and Timestamps.
2. **Banking Transactions (P2P Transfer)**:
   - Transfer money between accounts (Alice, Bob, Charlie, or custom accounts).
   - Smart contracts verify sufficient balance before transactions enter the mempool.
3. **Smart Contract Staking & Deposits**:
   - Locks principal for 6, 12, or 24 months with guaranteed yield calculation.
4. **Collateralized Micro-Loans**:
   - Smart contract calculates LTV (Loan-to-Value) and automatically disburses funds if collateral criteria are met.
5. **Interactive Mining (Proof-of-Work)**:
   - Click **"Mine Block (PoW)"** to execute the mining algorithm, calculate block hashes, and append transactions from the mempool to the chain.
6. **Security & Tamper Demonstration**:
   - Click **"Simulate Tamper Attack"** and modify an amount in an already-mined block.
   - The UI immediately changes to **TAMPER DETECTED / SECURITY ALERT**, showing which block and Merkle root failed integrity checks.
   - Click **"Restore Consensus"** to heal the ledger back to valid consensus.

---

## 📂 4. Project File Structure

```
mini project bct/
│
├── blockchain_core/
│   ├── __init__.py
│   ├── transaction.py        # Transaction structure & SHA-256 hashing
│   ├── block.py              # Block structure, Merkle Tree & Proof-of-Work
│   ├── smart_contract.py     # Banking logic & lending contracts
│   └── blockchain.py         # Ledger management, mempool, validation & tamper simulation
│
├── static/
│   ├── style.css             # Dark-themed modern dashboard styles
│   └── app.js                # Frontend reactive state controller
│
├── templates/
│   └── index.html            # Web dashboard interface
│
├── app.py                    # FastAPI server exposing REST & UI endpoints
├── Mini_Project_Report.md    # Complete academic project report aligned with college format
├── Mini_Project_Report_Format-Blockchain.docx  # Official University format template
└── README.md                 # Project documentation
```
