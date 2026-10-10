import hashlib
import json
import time
from typing import List, Dict, Any, Optional

class Transaction:
    """
    Represents a banking transaction in the decentralized ledger.
    Types: DEPOSIT, WITHDRAWAL, TRANSFER, LOAN_DISBURSE, LOAN_REPAY
    """
    def __init__(self, sender: str, recipient: str, amount: float, tx_type: str = "TRANSFER", metadata: Optional[Dict[str, Any]] = None, timestamp: Optional[float] = None):
        self.sender = sender          # 'SYSTEM' for deposits or interest, or user account address/name
        self.recipient = recipient    # Destination user account address/name
        self.amount = round(float(amount), 2)
        self.tx_type = tx_type        # DEPOSIT, WITHDRAWAL, TRANSFER, LOAN_DISBURSE, LOAN_REPAY
        self.metadata = metadata or {}
        self.timestamp = timestamp or time.time()
        self.tx_id = self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_id": self.tx_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "tx_type": self.tx_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }

    def calculate_hash(self) -> str:
        tx_data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "tx_type": self.tx_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
        encoded = json.dumps(tx_data, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        tx = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            tx_type=data.get("tx_type", "TRANSFER"),
            metadata=data.get("metadata", {}),
            timestamp=data.get("timestamp")
        )
        tx.tx_id = data.get("tx_id", tx.calculate_hash())
        return tx
