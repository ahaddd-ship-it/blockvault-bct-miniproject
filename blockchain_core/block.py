import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from blockchain_core.transaction import Transaction

class Block:
    """
    Represents an immutable ledger block storing batch banking transactions.
    """
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, nonce: int = 0, timestamp: Optional[float] = None, merkle_root: str = "", hash_val: str = ""):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp or time.time()
        self.merkle_root = merkle_root or self.compute_merkle_root()
        self.hash = hash_val or self.calculate_hash()

    def compute_merkle_root(self) -> str:
        """
        Calculates Merkle Root for fast transaction verification and integrity.
        """
        if not self.transactions:
            return hashlib.sha256(b"empty_block").hexdigest()
        
        tx_hashes = [tx.tx_id for tx in self.transactions]
        
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1]) # Duplicate last hash for odd counts
            
            new_level = []
            for i in range(0, len(tx_hashes), 2):
                combined = (tx_hashes[i] + tx_hashes[i+1]).encode()
                new_level.append(hashlib.sha256(combined).hexdigest())
            tx_hashes = new_level
            
        return tx_hashes[0]

    def calculate_hash(self) -> str:
        """
        Computes SHA-256 block hash.
        """
        block_string = json.dumps({
            "index": self.index,
            "merkle_root": self.merkle_root,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> int:
        """
        Proof of Work consensus algorithm. Finds nonce satisfying leading zeros target.
        """
        target = "0" * difficulty
        start_time = time.time()
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        mining_duration = round(time.time() - start_time, 4)
        return mining_duration

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [tx.to_dict() for tx in self.transactions]
        }
