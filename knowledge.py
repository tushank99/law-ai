"""Curated, hand-checked legal knowledge base.

The model may ONLY cite laws/sections that appear here. Anything else it says
about law must be framed as general guidance. Every entry should be re-verified
by a lawyer before production use.
"""

KB = {
    "security_deposit": {
        "title": "Landlord not returning security deposit",
        "keywords": ["deposit", "landlord", "rent", "tenant", "flat", "house owner", "advance",
                     "kiraya", "makan malik", "pg", "lease", "किराया", "मकान मालिक", "जमा", "डिपॉजिट"],
        "laws": [
            ("Indian Contract Act, 1872 - Section 73",
             "A party who suffers loss from breach of contract can claim compensation. The rent "
             "agreement is a contract; refusing to return the deposit is a breach."),
            ("Model Tenancy Act, 2021 - Section 11",
             "Caps residential security deposit at 2 months' rent and requires refund when the "
             "tenant hands over vacant possession, after lawful deductions. Applies ONLY in states "
             "that have adopted it - check your state's rent law."),
            ("Limitation Act, 1963",
             "A civil suit to recover money is generally to be filed within 3 years."),
        ],
        "steps": [
            "Collect: rent agreement, deposit payment proof (bank transfer/receipt), handover date, "
            "photos/video of flat at move-out, WhatsApp/SMS with landlord.",
            "Send a written demand (WhatsApp/email) asking for refund within 7-15 days.",
            "Send a formal legal notice (this app can draft one).",
            "If unpaid: file a civil recovery suit (Small Causes / Civil Court) or approach the "
            "Rent Authority if your state has one. Free legal aid is available via DLSA.",
        ],
        "lawyer_when": "Deposit is large, landlord claims damages/counter-claims, or you must go to court.",
    },
    "consumer_refund": {
        "title": "Refund / defective product / deficient service",
        "keywords": ["refund", "product", "order", "amazon", "flipkart", "defective", "service",
                     "warranty", "company", "online", "ecommerce", "delivery", "consumer", "bill",
                     "booking", "cancel", "airline", "flight", "replacement", "रिफंड", "सामान", "खराब"],
        "laws": [
            ("Consumer Protection Act, 2019 - Section 2(11)",
             "'Deficiency' means any fault, imperfection or shortcoming in the quality or manner "
             "of a service."),
            ("Consumer Protection Act, 2019 - Section 2(47)",
             "Defines 'unfair trade practice', including misleading claims and refusing to take "
             "back defective goods or refund as promised."),
            ("Consumer Protection Act, 2019 - Section 35",
             "A consumer can file a complaint before the District Consumer Commission."),
            ("Consumer Protection Act, 2019 - Section 69",
             "A complaint must be filed within 2 years of the cause of action."),
            ("Consumer Protection (E-Commerce) Rules, 2020",
             "E-commerce platforms must have a grievance officer and acknowledge complaints."),
        ],
        "steps": [
            "Collect: invoice/order ID, payment proof, photos of defect, chat/email with company.",
            "Complain to the company's customer care & grievance officer in writing; keep ticket numbers.",
            "Register with the National Consumer Helpline: call 1915 or consumerhelpline.gov.in.",
            "Send a legal notice giving 15 days to refund.",
            "File online at e-Daakhil (edaakhil.nic.in) before the District Commission - you can "
            "appear yourself without a lawyer for small claims.",
        ],
        "lawyer_when": "Large amounts, personal injury, or the company contests with lawyers.",
    },
    "unpaid_salary": {
        "title": "Salary / wages not paid",
        "keywords": ["salary", "wages", "employer", "job", "company not paying", "fired", "terminated",
                     "full and final", "f&f", "tankhwah", "naukri", "boss", "hr", "resign", "सैलरी", "वेतन", "तनख्वाह", "कंपनी", "नौकरी"],
        "laws": [
            ("Payment of Wages Act, 1936 / Code on Wages, 2019",
             "Wages must be paid on time without unauthorised deductions. The Code on Wages "
             "consolidates the older Act - check which applies to you and to your salary level."),
            ("Industrial Disputes Act, 1947 - Section 33C(2)",
             "A 'workman' can apply to the Labour Court to compute and recover money due from "
             "the employer. (Managers/supervisors may not qualify as workmen.)"),
            ("Indian Contract Act, 1872 - Section 73",
             "Non-payment of agreed salary is a breach of the employment contract; compensation "
             "can be claimed through a civil suit."),
        ],
        "steps": [
            "Collect: offer/appointment letter, salary slips, bank statements, attendance/emails "
            "proving work, resignation/termination letter.",
            "Write to HR/management by email asking for dues by a fixed date.",
            "File a grievance on the SAMADHAN portal (samadhan.labour.gov.in) or with the local "
            "Labour Commissioner office.",
            "Send a legal notice; then Labour Court (workmen) or civil suit (others).",
        ],
        "lawyer_when": "Termination dispute, large dues, or you are in a managerial role.",
    },
    "cheque_bounce": {
        "title": "Cheque bounced",
        "keywords": ["cheque", "check bounce", "bounced", "dishonour", "insufficient funds", "138", "चेक"],
        "laws": [
            ("Negotiable Instruments Act, 1881 - Section 138",
             "Dishonour of a cheque for insufficient funds, given to discharge a debt, is an "
             "offence. Payee must send a written demand notice within 30 days of receiving the "
             "bank's return memo; the drawer then has 15 days to pay."),
            ("Negotiable Instruments Act, 1881 - Section 142",
             "If not paid within those 15 days, the complaint must be filed in court within one "
             "month after the 15-day period ends."),
        ],
        "steps": [
            "Keep the original cheque and the bank's return memo.",
            "Send the demand notice within 30 days of the return memo (strict deadline!).",
            "If no payment in 15 days, file a complaint in the Magistrate court within 1 month.",
        ],
        "lawyer_when": "Almost always for filing the criminal complaint - deadlines are strict.",
    },
    "received_notice": {
        "title": "Received a legal notice I don't understand",
        "keywords": ["notice", "received", "summons", "court letter", "legal letter", "sent me a notice"],
        "laws": [],
        "steps": [
            "Do not ignore it. Note the date received and any deadline mentioned.",
            "Identify: who sent it, what they claim, what they demand, by when.",
            "Gather your documents and a timeline of your side.",
            "A notice is not a court order; a summons from a court is - that needs a lawyer urgently.",
            "Reply in writing (this app can draft a reply) or get a lawyer if money/property/criminal "
            "allegations are involved.",
        ],
        "lawyer_when": "Court summons, police matters, criminal allegations, or property disputes.",
    },
}

GENERAL = [
    ("Legal Services Authorities Act, 1987",
     "Free legal aid for eligible people (women, children, SC/ST, low-income, etc.) through "
     "NALSA / State / District Legal Services Authorities. NALSA helpline: 15100."),
]


def classify(text: str) -> list[str]:
    t = text.lower()
    scores = {k: sum(kw in t for kw in v["keywords"]) for k, v in KB.items()}
    hits = [k for k, s in sorted(scores.items(), key=lambda x: -x[1]) if s > 0]
    return hits[:2]


def context_for(categories: list[str]) -> str:
    out = []
    for c in categories:
        e = KB[c]
        out.append(f"## {e['title']}\nVERIFIED LAWS:")
        out += [f"- {n}: {d}" for n, d in e["laws"]] or ["- (none - give general guidance only)"]
        out.append("STEPS:")
        out += [f"- {s}" for s in e["steps"]]
        out.append(f"GET A LAWYER WHEN: {e['lawyer_when']}")
    out.append("## Always available\n" + "\n".join(f"- {n}: {d}" for n, d in GENERAL))
    return "\n".join(out)


def allowed_citations() -> set[str]:
    names = [n for e in KB.values() for n, _ in e["laws"]] + [n for n, _ in GENERAL]
    return set(names)
