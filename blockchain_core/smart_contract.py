from typing import Dict, Any, List

class SmartContractEngine:
    """
    Executes automated smart contracts for banking operations:
    1. Balance verification and auto-rejection of overdrafts
    2. Automated Fixed Deposit & Staking interest payouts
    3. Peer-to-Peer Micro-lending collateral & disbursement
    """
    def __init__(self):
        pass

    @staticmethod
    def validate_transfer(sender: str, amount: float, current_balance: float) -> (bool, str):
        if amount <= 0:
            return False, "Transfer amount must be strictly greater than zero."
        if sender != "SYSTEM" and current_balance < amount:
            return False, f"Contract Execution Reverted: Insufficient funds! Current balance: ${current_balance:.2f}, Required: ${amount:.2f}"
        return True, "Smart contract condition met: Transfer permitted."

    @staticmethod
    def process_fixed_deposit(account_name: str, principal: float, duration_months: int, interest_rate: float = 0.07) -> Dict[str, Any]:
        """
        Calculates maturity payout for an automated term deposit.
        """
        maturity_amount = round(principal * (1 + (interest_rate * (duration_months / 12.0))), 2)
        interest_earned = round(maturity_amount - principal, 2)
        return {
            "account": account_name,
            "principal": principal,
            "duration_months": duration_months,
            "interest_rate": f"{interest_rate * 100}%",
            "maturity_amount": maturity_amount,
            "interest_earned": interest_earned,
            "status": "LOCKED"
        }

    @staticmethod
    def evaluate_loan(borrower: str, requested_amount: float, collateral_amount: float, max_ltv: float = 0.70) -> (bool, str, float):
        """
        Collateralized micro-lending smart contract. Loan-to-Value (LTV) max 70%.
        """
        max_allowed_loan = round(collateral_amount * max_ltv, 2)
        if requested_amount <= 0:
            return False, "Invalid loan request amount.", 0.0
        if requested_amount > max_allowed_loan:
            return False, f"Contract Reverted: Insufficient collateral! Maximum borrowable: ${max_allowed_loan:.2f} for collateral of ${collateral_amount:.2f}", 0.0
        return True, f"Contract Approved: Loan of ${requested_amount:.2f} disbursed against collateral ${collateral_amount:.2f}.", requested_amount
