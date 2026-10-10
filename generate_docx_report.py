import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def generate_report():
    doc = docx.Document()

    # Configure base font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)

    # 1. Title Page
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("BLOCKVAULT: A DECENTRALIZED CORE BANKING LEDGER WITH SMART CONTRACT INTEGRATION\n\n")
    run_title.bold = True
    run_title.font.size = Pt(18)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.add_run("Submitted in partial fulfillment of the requirements\nof the Mini-Project of Blockchain Lab for Fourth Year of\nBachelors of Engineering\n\nby\n\n").italic = True
    
    student_p = doc.add_paragraph()
    student_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_st = student_p.add_run("Ahad, Owais, Saad\n(Roll No. _______)\n\n")
    run_st.bold = True
    run_st.font.size = Pt(13)

    dept_p = doc.add_paragraph()
    dept_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dept_p.add_run("Department of Artificial Intelligence & Data Science Engineering\nRizvi College of Engineering\nUniversity of Mumbai\n2026 - 2027\n")

    doc.add_page_break()

    # 2. Certificate
    cert_h = doc.add_heading("CERTIFICATE", level=1)
    cert_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    cert_p = doc.add_paragraph(
        "This is to certify that the mini-project entitled “BlockVault: A Decentralized Core Banking Ledger with Smart Contract Integration” "
        "is a bonafide work of Ahad, Owais, Saad (Roll No.: _______) submitted to the University of Mumbai in partial fulfillment "
        "of the requirement for the Mini-Project of Blockchain Lab for Fourth Year of the Bachelor of Engineering in “Artificial Intelligence & Data Science”.\n\n\n"
    )
    cert_p.paragraph_format.line_spacing = 1.5

    sign_table = doc.add_table(rows=2, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.rows[0].cells[0].paragraphs[0].text = "_________________________\nGuide / Prof. In-Charge"
    sign_table.rows[0].cells[1].paragraphs[0].text = "_________________________\nHead of Department (AI&DS)"
    sign_table.rows[1].cells[0].paragraphs[0].text = "\n\n_________________________\nInternal Examiner"
    sign_table.rows[1].cells[1].paragraphs[0].text = "\n\n_________________________\nDr. Varsha Shah (Principal, RCOE)"

    doc.add_page_break()

    # 3. Declaration
    dec_h = doc.add_heading("DECLARATION", level=1)
    dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(
        "I declare that this written submission represents my ideas in my own words and where others' ideas or words have been included, "
        "I have adequately cited and referenced the original sources. I also declare that I have adhered to all principles of academic "
        "honesty and integrity and have not misrepresented or fabricated or falsified any idea/data/fact/source in my submission. "
        "I understand that any violation of the above will be cause for disciplinary action by the Institute and can also evoke penal "
        "action from the sources which have thus not been properly cited or from whom proper permission has not been taken when needed.\n\n"
    )
    doc.add_paragraph("-----------------------------------------\n(Signature of Student)\n\nDate: _______________")

    doc.add_page_break()

    # 4. Abstract
    abs_h = doc.add_heading("ABSTRACT", level=1)
    abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(
        "Traditional centralized banking architectures suffer from single points of failure, opacity in interbank settlements, "
        "vulnerability to malicious insider database alterations, and high reconciliation overheads. This project, BlockVault, "
        "presents a decentralized core banking ledger prototype leveraging cryptographic hashing, immutable linked data structures, "
        "and automated smart contracts.\n\n"
        "BlockVault implements a distributed ledger powered by the SHA-256 algorithm and Proof-of-Work (PoW) consensus. Each block "
        "cryptographically seals transactions via a binary Merkle tree root, guaranteeing O(log n) tamper detection and lightweight proof "
        "of inclusion. In addition to peer-to-peer fund transfers, the platform incorporates programmatic smart contracts governing "
        "overdraft protection, interest-yielding term deposits, and collateralized micro-loans under strict loan-to-value (LTV) constraints. "
        "A visual dashboard provides interactive transaction broadcasting, block mining, and real-time ledger inspection. Furthermore, "
        "an attack simulation module allows intentional ledger tampering to empirically demonstrate the avalanche effect and the "
        "mathematical resilience of blockchain immutability."
    )

    doc.add_page_break()

    # 5. Index
    idx_h = doc.add_heading("INDEX", level=1)
    idx_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    index_table = doc.add_table(rows=12, cols=3)
    index_table.style = 'Table Grid'
    headers = ["Sr. No", "Title", "Page No"]
    for i, h in enumerate(headers):
        index_table.rows[0].cells[i].paragraphs[0].text = h
        index_table.rows[0].cells[i].paragraphs[0].runs[0].bold = True

    topics = [
        ("1.", "Introduction", "1"),
        ("2.", "System Analysis", "3"),
        ("3.", "System Design", "5"),
        ("4.", "Technologies Used", "8"),
        ("5.", "Implementation", "9"),
        ("6.", "Output Screenshots & Workflow", "12"),
        ("7.", "Testing & Validation", "14"),
        ("8.", "Results and Discussions", "16"),
        ("9.", "Conclusion and Future Scope", "18"),
        ("10.", "References", "19"),
        ("11.", "Appendix", "20")
    ]
    for row_idx, (sr, title, page) in enumerate(topics, start=1):
        index_table.rows[row_idx].cells[0].paragraphs[0].text = sr
        index_table.rows[row_idx].cells[1].paragraphs[0].text = title
        index_table.rows[row_idx].cells[2].paragraphs[0].text = page

    doc.add_page_break()

    # Section 1: Introduction
    doc.add_heading("1. Introduction", level=1)
    doc.add_heading("1.1 Background", level=2)
    doc.add_paragraph(
        "Conventional banking systems depend on centralized database architectures (e.g., Relational Database Management Systems "
        "managed by central bank administrators). While performant, centralized ledgers introduce distinct systemic risks:\n"
        "• Vulnerability to unauthorized database modifications (insider threats or cyber attacks).\n"
        "• Requirement of trusted central intermediaries for auditing and inter-bank clearing.\n"
        "• Disconnected silos requiring manual, expensive reconciliation processes."
    )
    doc.add_heading("1.2 Motivation", level=2)
    doc.add_paragraph(
        "Blockchain and distributed ledger technology (DLT) provide a paradigm shift by transitioning from 'trust through authority' "
        "to 'trust through cryptographic verification'. By combining public-key cryptography, linked list hashing, and consensus protocols, "
        "blockchain enables mutually untrusted parties to maintain a single, synchronized, and tamper-resistant truth."
    )
    doc.add_heading("1.3 Problem Statement", level=2)
    doc.add_paragraph(
        "To design and build an educational yet functional decentralized core banking prototype (BlockVault) that models peer-to-peer "
        "banking settlements, demonstrates the cryptographic integrity of blockchain blocks, enforces autonomous smart contract banking rules, "
        "and offers visual proof of immutability against malicious data tampering."
    )

    # Section 2: System Analysis
    doc.add_heading("2. System Analysis", level=1)
    doc.add_paragraph(
        "A rigorous comparative analysis was performed contrasting traditional centralized core banking ledgers against the proposed decentralized architecture:"
    )
    comp_table = doc.add_table(rows=6, cols=3)
    comp_table.style = 'Table Grid'
    comp_headers = ["Parameter", "Traditional Banking Ledger", "BlockVault Blockchain Ledger"]
    for i, h in enumerate(comp_headers):
        comp_table.rows[0].cells[i].paragraphs[0].text = h
        comp_table.rows[0].cells[i].paragraphs[0].runs[0].bold = True

    comp_data = [
        ("Storage Paradigm", "Centralized SQL / Oracle DB", "Cryptographically chained blocks"),
        ("Trust & Security", "Administrative access control", "SHA-256 hashes & PoW consensus"),
        ("Tamper Resistance", "Vulnerable to root DB updates", "Mathematically irreversible"),
        ("Reconciliation", "Manual batch reconciliation", "Zero-reconciliation instant truth"),
        ("Automation", "Server cron jobs & scripts", "Deterministic smart contracts")
    ]
    for row_idx, (p, c, b) in enumerate(comp_data, start=1):
        comp_table.rows[row_idx].cells[0].paragraphs[0].text = p
        comp_table.rows[row_idx].cells[1].paragraphs[0].text = c
        comp_table.rows[row_idx].cells[2].paragraphs[0].text = b

    # Section 3: System Design
    doc.add_heading("3. System Design", level=1)
    doc.add_paragraph(
        "The architecture is organized into four distinct operational layers:\n"
        "1. Presentation Layer: Modern dark-themed dashboard featuring real-time transaction forms, mining trigger, and live ledger visualizer.\n"
        "2. Service / API Layer: Asynchronous FastAPI endpoints handling JSON payloads for transactions, mining, smart contracts, and tampering.\n"
        "3. Smart Contract Engine: Autonomous execution logic for balance verification, term deposits (7% APY), and micro-loans (70% LTV).\n"
        "4. Blockchain Core Layer: Proof-of-Work engine, binary Merkle tree calculator, SHA-256 block hash generator, and persistent JSON ledger."
    )

    # Section 4: Technologies Used
    doc.add_heading("4. Technologies Used", level=1)
    doc.add_paragraph(
        "• Python 3.11: Core language powering blockchain algorithms, cryptography, and business logic.\n"
        "• FastAPI & Uvicorn: High-speed asynchronous ASGI web framework.\n"
        "• SHA-256 & Hashlib: Standard cryptographic digest for block headers and Merkle trees.\n"
        "• HTML5 / CSS3 / Bootstrap 5: Responsive frontend UI for academic presentation.\n"
        "• JavaScript (ES6+): Client-side reactive dashboard and state synchronizer."
    )

    # Section 5: Implementation
    doc.add_heading("5. Implementation", level=1)
    doc.add_paragraph(
        "Key implementation modules:\n"
        "• Transaction Class: Models sender, recipient, amount, transaction type, and SHA-256 tx_id.\n"
        "• Block Class: Handles previous_hash linking, nonce mining loop, and recursive Merkle root hashing.\n"
        "• Smart Contract Class: Evaluates collateralization limits and interest formulas.\n"
        "• Blockchain Class: Manages chain integrity validation, mempool, genesis block seeding, and tamper attacks."
    )

    # Section 6: Testing & Validation
    doc.add_heading("6. Testing & Validation", level=1)
    doc.add_paragraph(
        "System tests were carried out covering normal banking operations as well as adversarial attacks. All 7 test cases passed successfully:\n"
        "1. Genesis Block Seeding: PASS\n"
        "2. Peer-to-Peer Transfer: PASS\n"
        "3. Overdraft Rejection: PASS\n"
        "4. Proof-of-Work Nonce Mining: PASS\n"
        "5. Merkle Root Integrity Validation: PASS\n"
        "6. Adversarial Tamper Attack Detection: PASS\n"
        "7. Consensus Recovery: PASS"
    )

    # Section 7: Conclusion
    doc.add_heading("7. Conclusion", level=1)
    doc.add_paragraph(
        "BlockVault successfully proves the viability and security of decentralized ledger technology in banking applications. "
        "Through autonomous smart contracts, Merkle trees, and cryptographic Proof-of-Work, the prototype provides a transparent, "
        "tamper-resistant alternative to legacy centralized banking systems."
    )

    doc.add_heading("8. References", level=1)
    doc.add_paragraph(
        "1. Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System.\n"
        "2. Antonopoulos, A. M. (2017). Mastering Bitcoin: Programming the Open Blockchain. O'Reilly Media.\n"
        "3. Wood, G. (2014). Ethereum: A Secure Decentralised Generalised Transaction Ledger.\n"
        "4. Tapscott, D., & Tapscott, A. (2016). Blockchain Revolution."
    )

    output_path = "Mini_Project_Report_BlockVault.docx"
    doc.save(output_path)
    print("Report saved successfully as:", output_path)

if __name__ == "__main__":
    generate_report()
