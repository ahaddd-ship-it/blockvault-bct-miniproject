// BlockVault JavaScript Client

let tamperModalInstance = null;
let newAccountModalInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    tamperModalInstance = new bootstrap.Modal(document.getElementById('tamperModal'));
    newAccountModalInstance = new bootstrap.Modal(document.getElementById('newAccountModal'));
    fetchLedgerState();
});

async function fetchLedgerState() {
    try {
        const response = await fetch('/api/state');
        const data = await response.json();
        
        // Update top statistics
        document.getElementById('statBlockCount').innerText = data.chain.length;
        document.getElementById('statMempoolCount').innerText = data.mempool.length;
        document.getElementById('statAccountCount').innerText = Object.keys(data.balances).length;
        document.getElementById('mempoolBadge').innerText = data.mempool.length;

        // Update Chain Integrity Indicator
        const badge = document.getElementById('chainStatusBadge');
        const alertBox = document.getElementById('chainIntegrityAlert');
        const alertMsg = document.getElementById('chainIntegrityMsg');

        if (data.is_valid) {
            badge.className = "badge bg-success px-3 py-2 fs-6";
            badge.innerHTML = '<i class="fa-solid fa-shield-halved me-1"></i> Ledger Verified';
            alertBox.className = "alert alert-success d-flex align-items-center py-2 mb-3";
            alertBox.innerHTML = `<i class="fa-solid fa-circle-check fs-5 me-2"></i><span>${data.validation_msg}</span>`;
        } else {
            badge.className = "badge bg-danger px-3 py-2 fs-6 animate-pulse";
            badge.innerHTML = '<i class="fa-solid fa-triangle-exclamation me-1"></i> Tamper Detected!';
            alertBox.className = "alert alert-danger d-flex align-items-center py-2 mb-3";
            alertBox.innerHTML = `<i class="fa-solid fa-triangle-exclamation fs-5 me-2"></i><strong>SECURITY ALERT:</strong>&nbsp;<span>${data.validation_msg}</span>`;
        }

        // Render account balances
        renderBalances(data.balances);

        // Render sender selectors
        renderAccountDropdowns(Object.keys(data.balances));

        // Render mempool
        renderMempool(data.mempool);

        // Render blocks
        renderBlockchain(data.chain, data.is_valid);

    } catch (err) {
        console.error("Failed to load blockchain state:", err);
    }
}

function renderBalances(balances) {
    const tbody = document.getElementById('balancesTableBody');
    tbody.innerHTML = '';
    for (const [account, bal] of Object.entries(balances)) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <span class="badge bg-secondary me-2"><i class="fa-solid fa-user"></i></span>
                <span class="fw-semibold text-light">${account}</span>
            </td>
            <td class="text-end fw-bold font-monospace text-success">₹${bal.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        `;
        tbody.appendChild(tr);
    }
}

function renderAccountDropdowns(accounts) {
    const dropdowns = ['transferSender', 'depositAccount', 'loanBorrower'];
    dropdowns.forEach(id => {
        const el = document.getElementById(id);
        const currentVal = el.value;
        el.innerHTML = '<option value="" disabled selected>Select Account</option>';
        accounts.forEach(acc => {
            const opt = document.createElement('option');
            opt.value = acc;
            opt.innerText = acc;
            if (acc === currentVal) opt.selected = true;
            el.appendChild(opt);
        });
        if (!el.value && accounts.length > 0) {
            el.selectedIndex = 1;
        }
    });
}

function renderMempool(mempool) {
    const container = document.getElementById('mempoolContainer');
    container.innerHTML = '';
    if (mempool.length === 0) {
        container.innerHTML = '<div class="text-center text-muted py-4 font-sm"><i class="fa-solid fa-circle-notch fa-spin me-1"></i> No pending transactions in mempool.</div>';
        return;
    }

    mempool.forEach(tx => {
        const div = document.createElement('div');
        div.className = 'tx-pill d-flex justify-content-between align-items-center';
        div.innerHTML = `
            <div>
                <span class="badge bg-primary font-sm me-1">${tx.tx_type}</span>
                <span class="fw-semibold text-light">${tx.sender}</span>
                <i class="fa-solid fa-arrow-right text-muted mx-1 font-sm"></i>
                <span class="fw-semibold text-light">${tx.recipient}</span>
                ${tx.metadata && tx.metadata.note ? `<div class="text-muted font-sm">${tx.metadata.note}</div>` : ''}
            </div>
            <span class="fw-bold text-warning font-monospace">₹${tx.amount.toLocaleString('en-IN', {minimumFractionDigits: 2})}</span>
        `;
        container.appendChild(div);
    });
}

function renderBlockchain(chain, isValid) {
    const container = document.getElementById('blockchainTimeline');
    container.innerHTML = '';

    // Render from newest block to genesis
    for (let i = chain.length - 1; i >= 0; i--) {
        const block = chain[i];
        const blockEl = document.createElement('div');
        blockEl.className = 'block-card mb-2';

        const txList = block.transactions.map((tx, txIdx) => `
            <div class="d-flex justify-content-between align-items-center font-sm border-bottom border-secondary py-1">
                <div>
                    <span class="badge bg-secondary font-sm me-1">#${txIdx} ${tx.tx_type}</span>
                    <span class="text-light">${tx.sender} &rarr; ${tx.recipient}</span>
                </div>
                <span class="font-monospace text-info fw-semibold">₹${tx.amount.toLocaleString('en-IN', {minimumFractionDigits: 2})}</span>
            </div>
        `).join('');

        blockEl.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="fw-bold text-primary">
                    <i class="fa-solid fa-cube me-1"></i> Block #${block.index} ${block.index === 0 ? '<span class="badge bg-info">Genesis</span>' : ''}
                </span>
                <div class="font-sm text-muted">
                    <i class="fa-solid fa-clock me-1"></i> ${new Date(block.timestamp * 1000).toLocaleTimeString()}
                    <span class="badge bg-dark border border-secondary ms-2">Nonce: ${block.nonce}</span>
                </div>
            </div>

            <div class="mb-2">
                <div class="font-sm text-muted mb-1">Previous Hash:</div>
                <div class="hash-badge prev">${block.previous_hash}</div>
            </div>

            <div class="mb-2">
                <div class="font-sm text-muted mb-1">Merkle Root:</div>
                <div class="hash-badge merkle">${block.merkle_root}</div>
            </div>

            <div class="mb-2">
                <div class="font-sm text-muted mb-1">Block Hash (SHA-256):</div>
                <div class="hash-badge current">${block.hash}</div>
            </div>

            <div class="mt-3">
                <div class="font-sm fw-bold text-muted mb-1"><i class="fa-solid fa-list-check me-1"></i> Transactions (${block.transactions.length})</div>
                <div class="bg-dark p-2 rounded">${txList}</div>
            </div>
        `;

        container.appendChild(blockEl);

        if (i > 0) {
            const arrow = document.createElement('div');
            arrow.className = 'chain-arrow my-2';
            arrow.innerHTML = '<i class="fa-solid fa-link"></i> Cryptographically Chained';
            container.appendChild(arrow);
        }
    }
}

async function submitTransfer(e) {
    e.preventDefault();
    const payload = {
        sender: document.getElementById('transferSender').value,
        recipient: document.getElementById('transferRecipient').value,
        amount: parseFloat(document.getElementById('transferAmount').value),
        note: document.getElementById('transferNote').value,
        tx_type: "TRANSFER"
    };

    const res = await fetch('/api/transaction', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) 
    });
    const result = await res.json();
    if (!res.ok) {
        alert("Transaction Failed: " + result.message);
    } else {
        document.getElementById('transferAmount').value = '';
        document.getElementById('transferNote').value = '';
        fetchLedgerState();
    }
}

async function submitTermDeposit(e) {
    e.preventDefault();
    const payload = {
        account: document.getElementById('depositAccount').value,
        amount: parseFloat(document.getElementById('depositAmount').value),
        duration_months: parseInt(document.getElementById('depositMonths').value)
    };

    const res = await fetch('/api/smart-contract/term-deposit', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) 
    });
    const result = await res.json();
    if (!res.ok) {
        alert("Smart Contract Execution Failed: " + result.message);
    } else {
        alert("Deposit Locked via Smart Contract! Expected yield payout: ₹" + result.contract.maturity_amount.toLocaleString('en-IN'));
        document.getElementById('depositAmount').value = '';
        fetchLedgerState();
    }
}

async function submitLoan(e) {
    e.preventDefault();
    const payload = {
        borrower: document.getElementById('loanBorrower').value,
        collateral_amount: parseFloat(document.getElementById('loanCollateral').value),
        loan_amount: parseFloat(document.getElementById('loanAmount').value)
    };

    const res = await fetch('/api/smart-contract/micro-loan', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) 
    });
    const result = await res.json();
    if (!res.ok) {
        alert("Loan Request Rejected: " + result.message);
    } else {
        alert(result.message);
        document.getElementById('loanCollateral').value = '';
        document.getElementById('loanAmount').value = '';
        fetchLedgerState();
    }
}

async function mineBlock() {
    const payload = { miner: "Validator_Node_1" };

    const res = await fetch('/api/mine', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) 
    });
    const result = await res.json();
    if (!res.ok) {
        alert(result.message);
    } else {
        alert(`Block #${result.block_index} successfully mined in ${result.mining_time_seconds}s! Nonce found: ${result.nonce}`);
        fetchLedgerState();
    }
}

function triggerTamperModal() {
    tamperModalInstance.show();
}

async function executeTamper() {
    const payload = {
        block_index: parseInt(document.getElementById('tamperBlockIndex').value),
        tx_index: parseInt(document.getElementById('tamperTxIndex').value),
        new_amount: parseFloat(document.getElementById('tamperAmount').value)
    };

    const res = await fetch('/api/tamper', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) 
    });
    const result = await res.json();
    tamperModalInstance.hide();
    alert("Attack Executed! " + result.message + " Notice how the chain integrity status immediately flags the violation.");
    fetchLedgerState();
}

async function repairLedger() {
    const res = await fetch('/api/repair', { method: 'POST' });
    const result = await res.json();
    alert(result.message);
    fetchLedgerState();
}

async function createNewAccount() {
    const name = document.getElementById('newAccountName').value.trim();
    const amount = parseFloat(document.getElementById('newAccountInitial').value);
    if (!name) return;

    const payload = { account: name, amount: amount };

    const res = await fetch('/api/fund', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) 
    });
    newAccountModalInstance.hide();
    document.getElementById('newAccountName').value = '';
    fetchLedgerState();
}
