import json
import os
import time
from typing import List, Dict, Any, Optional
from blockchain_core.block import Block
from blockchain_core.transaction import Transaction
from blockchain_core.smart_contract import SmartContractEngine

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "..", "ledger_storage.json")

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.unconfirmed_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.smart_contract = SmartContractEngine()
        self.load_chain()

    def create_genesis_block(self):
        """
        Generates the first block in the blockchain ledger with initial system setup.
        """
        genesis_tx = Transaction(
            sender="GENESIS",
            recipient="SYSTEM_RESERVE",
            amount=1000000.0,
            tx_type="GENESIS",
            metadata={"note": "Initial Central Reserve Protocol Fund"}
        )
        genesis_block = Block(
            index=0,
            transactions=[genesis_tx],
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        
        # Initial accounts seeding for demonstration
        self.fund_account("ahad", 50000.0)
        self.fund_account("owais", 35000.0)
        self.fund_account("saad", 20000.0)
        self.mine_pending_transactions(miner_address="SYSTEM")
        self.save_chain()

    def fund_account(self, recipient: str, amount: float):
        tx = Transaction(
            sender="SYSTEM_RESERVE",
            recipient=recipient,
            amount=amount,
            tx_type="DEPOSIT",
            metadata={"note": f"Initial banking deposit for {recipient}"}
        )
        self.unconfirmed_transactions.append(tx)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float, tx_type: str = "TRANSFER", metadata: Optional[Dict[str, Any]] = None) -> (bool, str):
        """
        Validates transaction through smart contract logic before accepting to mempool.
        """
        sender_bal = self.get_balance(sender)
        
        if tx_type == "TRANSFER":
            valid, msg = self.smart_contract.validate_transfer(sender, amount, sender_bal)
            if not valid:
                return False, msg

        tx = Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            tx_type=tx_type,
            metadata=metadata or {}
        )
        self.unconfirmed_transactions.append(tx)
        return True, f"Transaction {tx.tx_id[:8]} added to memory pool."

    def mine_pending_transactions(self, miner_address: str = "Miner_Node_1") -> Dict[str, Any]:
        """
        Packs mempool transactions into a new Block, runs Proof of Work, and appends to ledger.
        """
        if not self.unconfirmed_transactions:
            return {"status": "error", "message": "No pending transactions to mine."}

        # Reward transaction for miner (Proof of Work incentive)
        reward_tx = Transaction(
            sender="SYSTEM",
            recipient=miner_address,
            amount=10.0,
            tx_type="MINING_REWARD",
            metadata={"note": f"Proof-of-Work Block Reward for Node {miner_address}"}
        )
        txs_to_mine = list(self.unconfirmed_transactions)
        txs_to_mine.append(reward_tx)

        new_block = Block(
            index=len(self.chain),
            transactions=txs_to_mine,
            previous_hash=self.last_block.hash
        )

        mining_duration = new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        self.save_chain()

        return {
            "status": "success",
            "message": f"Block #{new_block.index} successfully mined!",
            "block_index": new_block.index,
            "block_hash": new_block.hash,
            "nonce": new_block.nonce,
            "mining_time_seconds": mining_duration,
            "tx_count": len(new_block.transactions)
        }

    def get_balance(self, account: str) -> float:
        """
        Audits the entire blockchain ledger history to compute account balance.
        """
        balance = 0.0
        # Audit mined transactions
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == account:
                    balance += tx.amount
                if tx.sender == account:
                    balance -= tx.amount

        # Also account for pending transactions in mempool
        for tx in self.unconfirmed_transactions:
            if tx.sender == account:
                balance -= tx.amount
        return round(balance, 2)

    def get_all_accounts(self) -> List[str]:
        accounts = set()
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender and tx.sender not in ["GENESIS", "SYSTEM"]:
                    accounts.add(tx.sender)
                if tx.recipient and tx.recipient not in ["SYSTEM_RESERVE"]:
                    accounts.add(tx.recipient)
        return sorted(list(accounts))

    def is_chain_valid(self) -> (bool, str):
        """
        Validates cryptographic integrity of the blockchain:
        1. Validates each block's cryptographic hash matches its contents
        2. Validates block links (previous_hash matches predecessor)
        3. Validates Merkle Root of each block
        4. Validates Proof-of-Work difficulty target
        """
        target = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Verify link
            if current.previous_hash != previous.hash:
                return False, f"Broken Chain: Block #{current.index} previous_hash mismatch! Linked: {current.previous_hash[:10]}... Expected: {previous.hash[:10]}..."

            # 2. Verify Merkle Root
            expected_merkle = current.compute_merkle_root()
            if current.merkle_root != expected_merkle:
                return False, f"Tampered Data: Block #{current.index} Merkle root invalid! Contains altered transaction."

            # 3. Verify Block Hash recalculation
            if current.hash != current.calculate_hash():
                return False, f"Tampered Data: Block #{current.index} calculated hash does not match stored hash."

            # 4. Verify Proof of work
            if not current.hash.startswith(target):
                return False, f"Invalid Proof of Work: Block #{current.index} does not satisfy difficulty target."

        return True, "Blockchain integrity 100% verified. All cryptographic proofs valid."

    def tamper_block(self, block_index: int, tx_index: int, new_amount: float) -> (bool, str):
        """
        Simulate malicious attack: Modifies an amount in an existing mined block.
        Demonstrates how blockchain immediately detects tampering!
        """
        if block_index <= 0 or block_index >= len(self.chain):
            return False, "Invalid block index or cannot tamper genesis block."

        block = self.chain[block_index]
        if tx_index < 0 or tx_index >= len(block.transactions):
            return False, "Invalid transaction index."

        original_amount = block.transactions[tx_index].amount
        block.transactions[tx_index].amount = new_amount
        # Note: We intentionally DO NOT recompute hash or re-mine so the anomaly is detectable
        return True, f"Block #{block_index} Tx #{tx_index} hacked! Amount changed from ${original_amount} to ${new_amount}."

    def repair_chain(self):
        """
        Restores chain from clean persisted state.
        """
        self.load_chain()

    def to_dict(self) -> List[Dict[str, Any]]:
        return [block.to_dict() for block in self.chain]

    def save_chain(self):
        try:
            data = {
                "difficulty": self.difficulty,
                "chain": [b.to_dict() for b in self.chain]
            }
            with open(LEDGER_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Error saving ledger:", e)

    def load_chain(self):
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, "r") as f:
                    data = json.load(f)
                    self.difficulty = data.get("difficulty", 2)
                    self.chain = []
                    for b_data in data.get("chain", []):
                        txs = [Transaction.from_dict(t) for t in b_data.get("transactions", [])]
                        block = Block(
                            index=b_data["index"],
                            transactions=txs,
                            previous_hash=b_data["previous_hash"],
                            nonce=b_data["nonce"],
                            timestamp=b_data["timestamp"],
                            merkle_root=b_data.get("merkle_root", ""),
                            hash_val=b_data.get("hash", "")
                        )
                        self.chain.append(block)
                if not self.chain:
                    self.create_genesis_block()
            except Exception as e:
                print("Error loading ledger, recreating genesis:", e)
                self.create_genesis_block()
        else:
            self.create_genesis_block()
