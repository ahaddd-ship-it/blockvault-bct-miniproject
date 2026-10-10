import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from blockchain_core.blockchain import Blockchain
from blockchain_core.smart_contract import SmartContractEngine

app = FastAPI(title="BlockVault: Decentralized Core Banking Ledger")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

blockchain = Blockchain(difficulty=2)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "chain": blockchain.chain,
            "mempool": blockchain.unconfirmed_transactions,
            "accounts": blockchain.get_all_accounts(),
            "difficulty": blockchain.difficulty
        }
    )

@app.get("/api/state")
async def get_state():
    accounts_balance = {acc: blockchain.get_balance(acc) for acc in blockchain.get_all_accounts()}
    valid, msg = blockchain.is_chain_valid()
    return JSONResponse({
        "chain": [b.to_dict() for b in blockchain.chain],
        "mempool": [tx.to_dict() for tx in blockchain.unconfirmed_transactions],
        "balances": accounts_balance,
        "is_valid": valid,
        "validation_msg": msg,
        "difficulty": blockchain.difficulty
    })

from pydantic import BaseModel

class TxRequest(BaseModel):
    sender: str
    recipient: str
    amount: float
    tx_type: str = "TRANSFER"
    note: str = ""

class MineRequest(BaseModel):
    miner: str = "Miner_Node_1"

class TermDepositRequest(BaseModel):
    account: str
    amount: float
    duration_months: int

class MicroLoanRequest(BaseModel):
    borrower: str
    loan_amount: float
    collateral_amount: float

class TamperRequest(BaseModel):
    block_index: int
    tx_index: int
    new_amount: float

class FundRequest(BaseModel):
    account: str
    amount: float

@app.post("/api/transaction")
async def create_transaction(req: TxRequest):
    if req.sender == req.recipient:
        return JSONResponse({"status": "error", "message": "Sender and recipient cannot be the same address."}, status_code=400)
    
    success, msg = blockchain.add_transaction(
        sender=req.sender,
        recipient=req.recipient,
        amount=req.amount,
        tx_type=req.tx_type,
        metadata={"note": req.note}
    )
    if not success:
        return JSONResponse({"status": "error", "message": msg}, status_code=400)
    
    return JSONResponse({"status": "success", "message": msg})

@app.post("/api/mine")
async def mine_block(req: MineRequest = MineRequest()):
    result = blockchain.mine_pending_transactions(miner_address=req.miner)
    if result["status"] == "error":
        return JSONResponse(result, status_code=400)
    return JSONResponse(result)

@app.post("/api/smart-contract/term-deposit")
async def term_deposit(req: TermDepositRequest):
    current_bal = blockchain.get_balance(req.account)
    if current_bal < req.amount:
        return JSONResponse({"status": "error", "message": f"Insufficient funds to open term deposit. Balance: ${current_bal}"}, status_code=400)

    contract_details = SmartContractEngine.process_fixed_deposit(req.account, req.amount, req.duration_months)
    success, msg = blockchain.add_transaction(
        sender=req.account,
        recipient="VAULT_STAKING_CONTRACT",
        amount=req.amount,
        tx_type="STAKING_DEPOSIT",
        metadata=contract_details
    )
    return JSONResponse({"status": "success", "contract": contract_details, "message": msg})

@app.post("/api/smart-contract/micro-loan")
async def micro_loan(req: MicroLoanRequest):
    valid, msg, approved_amount = SmartContractEngine.evaluate_loan(req.borrower, req.loan_amount, req.collateral_amount)
    if not valid:
        return JSONResponse({"status": "error", "message": msg}, status_code=400)

    blockchain.add_transaction(
        sender="SYSTEM_RESERVE",
        recipient=req.borrower,
        amount=approved_amount,
        tx_type="LOAN_DISBURSE",
        metadata={"collateral": req.collateral_amount, "ltv": "70%"}
    )
    return JSONResponse({"status": "success", "message": msg})

@app.post("/api/tamper")
async def tamper_data(req: TamperRequest):
    success, msg = blockchain.tamper_block(req.block_index, req.tx_index, req.new_amount)
    if not success:
        return JSONResponse({"status": "error", "message": msg}, status_code=400)
    return JSONResponse({"status": "tampered", "message": msg})

@app.post("/api/repair")
async def repair_blockchain():
    blockchain.repair_chain()
    return JSONResponse({"status": "success", "message": "Blockchain state restored to verified consensus."})

@app.post("/api/fund")
async def fund_account_api(req: FundRequest):
    blockchain.fund_account(req.account, req.amount)
    return JSONResponse({"status": "success", "message": f"Funded {req.account} with ${req.amount:.2f}."})

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
