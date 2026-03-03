#!/usr/bin/env python3
"""
Risk Assessment Tool — Educational Exercise
Demonstrates GRC concepts: risk scoring (Likelihood × Impact),
risk registers, severity levels, and risk response strategies.
"""

import json
import os
import sys
from datetime import date

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║          RISK ASSESSMENT TOOL — Educational                 ║
║    Risk Register · Scoring · Severity · Response Strategy   ║
╚══════════════════════════════════════════════════════════════╝
"""

SEVERITY = {
    (1, 4):  ("LOW",      "Accept — monitor periodically"),
    (5, 9):  ("MEDIUM",   "Mitigate — apply controls within 90 days"),
    (10,14): ("HIGH",     "Mitigate — apply controls within 30 days"),
    (15,25): ("CRITICAL", "Immediate action — escalate to management"),
}

REGISTER_FILE = "risk_register.json"
register = []

def get_severity(score):
    for (low, high), (level, response) in SEVERITY.items():
        if low <= score <= high:
            return level, response
    return "UNKNOWN", "Review manually"

def load_register():
    global register
    if os.path.exists(REGISTER_FILE):
        try:
            with open(REGISTER_FILE) as f:
                register = json.load(f)
            print(f"[+] Loaded {len(register)} risk(s) from {REGISTER_FILE}")
        except Exception:
            register = []

def save_register():
    with open(REGISTER_FILE, "w") as f:
        json.dump(register, f, indent=2)
    print(f"[+] Risk register saved to {REGISTER_FILE}")

def add_risk():
    """Add a new risk entry to the register."""
    print("\n  [*] Add New Risk\n")
    asset     = input("  Asset (e.g. Customer Database): ").strip()
    threat    = input("  Threat (e.g. SQL Injection): ").strip()
    vuln      = input("  Vulnerability (e.g. Unvalidated input): ").strip()

    print("\n  Likelihood — how likely is this threat to occur?")
    print("  1=Rare  2=Unlikely  3=Possible  4=Likely  5=Almost Certain")
    try:
        likelihood = int(input("  Likelihood [1-5]: ").strip())
        if not 1 <= likelihood <= 5:
            raise ValueError
    except ValueError:
        print("[!] Invalid. Enter a number 1-5."); return

    print("\n  Impact — what is the potential damage if this occurs?")
    print("  1=Negligible  2=Minor  3=Moderate  4=Major  5=Catastrophic")
    try:
        impact = int(input("  Impact [1-5]: ").strip())
        if not 1 <= impact <= 5:
            raise ValueError
    except ValueError:
        print("[!] Invalid. Enter a number 1-5."); return

    score = likelihood * impact
    severity, response = get_severity(score)

    risk = {
        "id": len(register) + 1,
        "date": str(date.today()),
        "asset": asset,
        "threat": threat,
        "vulnerability": vuln,
        "likelihood": likelihood,
        "impact": impact,
        "score": score,
        "severity": severity,
        "response": response,
        "status": "Open"
    }
    register.append(risk)
    save_register()

    print(f"""
  ┌─────────────────────────────────────────────┐
  │  Risk #{risk['id']} Added                           │
  └─────────────────────────────────────────────┘
  Score    : {likelihood} × {impact} = {score}
  Severity : {severity}
  Response : {response}""")

def view_register():
    """Display the full risk register as a table."""
    if not register:
        print("\n[!] Risk register is empty. Add risks first.")
        return

    print(f"\n  {'ID':<4} {'Severity':<10} {'Score':<6} {'Asset':<22} {'Threat':<25} {'Status'}")
    print(f"  {'─'*3} {'─'*9} {'─'*5} {'─'*21} {'─'*24} {'─'*8}")

    for r in sorted(register, key=lambda x: x["score"], reverse=True):
        sev = r["severity"]
        marker = "!!" if sev == "CRITICAL" else "! " if sev == "HIGH" else "  "
        print(f"  {r['id']:<4} {sev:<10} {r['score']:<6} {r['asset']:<22} {r['threat']:<25} {r['status']}")

    print(f"\n  [+] Total risks: {len(register)}")
    critical = sum(1 for r in register if r["severity"] == "CRITICAL")
    high     = sum(1 for r in register if r["severity"] == "HIGH")
    if critical: print(f"  [!] CRITICAL: {critical} risk(s) require immediate action")
    if high:     print(f"  [!] HIGH:     {high} risk(s) require action within 30 days")

def view_risk_detail():
    """Show full detail for a single risk entry."""
    try:
        rid = int(input("\n[?] Enter Risk ID to view: ").strip())
    except ValueError:
        print("[!] Invalid ID."); return

    risk = next((r for r in register if r["id"] == rid), None)
    if not risk:
        print(f"[!] Risk #{rid} not found."); return

    print(f"""
  ┌─────────────────────────────────────────────────────┐
  │  Risk #{risk['id']} — {risk['severity']}                         │
  └─────────────────────────────────────────────────────┘
  Date          : {risk['date']}
  Asset         : {risk['asset']}
  Threat        : {risk['threat']}
  Vulnerability : {risk['vulnerability']}
  Likelihood    : {risk['likelihood']}/5
  Impact        : {risk['impact']}/5
  Risk Score    : {risk['score']}/25
  Severity      : {risk['severity']}
  Response      : {risk['response']}
  Status        : {risk['status']}""")

def risk_matrix():
    """Display a 5×5 risk matrix with current risks mapped."""
    print("""
  ┌─────────────────────────────────────────────────────┐
  │            5×5 Risk Matrix                          │
  │    Likelihood (rows) × Impact (columns)             │
  └─────────────────────────────────────────────────────┘

           Impact →
           1-Neg  2-Min  3-Mod  4-Maj  5-Cat
  Like ↓  ┌──────┬──────┬──────┬──────┬──────┐
  5-ACert │  5   │  10  │  15  │  20  │  25  │ CRITICAL
          ├──────┼──────┼──────┼──────┼──────┤
  4-Likely│  4   │   8  │  12  │  16  │  20  │ HIGH
          ├──────┼──────┼──────┼──────┼──────┤
  3-Poss  │  3   │   6  │   9  │  12  │  15  │ HIGH/MED
          ├──────┼──────┼──────┼──────┼──────┤
  2-Unlik │  2   │   4  │   6  │   8  │  10  │ MEDIUM
          ├──────┼──────┼──────┼──────┼──────┤
  1-Rare  │  1   │   2  │   3  │   4  │   5  │ LOW
          └──────┴──────┴──────┴──────┴──────┘

  Score ranges:
    1–4   LOW      Accept — monitor periodically
    5–9   MEDIUM   Mitigate within 90 days
    10–14 HIGH     Mitigate within 30 days
    15–25 CRITICAL Immediate escalation required
""")

def main():
    print(BANNER)
    load_register()
    print()
    while True:
        print("  Options:")
        print("  1. Add a risk to the register")
        print("  2. View risk register (all risks)")
        print("  3. View risk detail")
        print("  4. View risk matrix (scoring guide)")
        print("  0. Exit\n")
        choice = input("[?] Select option: ").strip()
        print()
        if   choice == "1": add_risk()
        elif choice == "2": view_register()
        elif choice == "3": view_risk_detail()
        elif choice == "4": risk_matrix()
        elif choice == "0": print("[+] Goodbye.\n"); sys.exit(0)
        else: print("[!] Invalid option.")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted.\n")
        sys.exit(0)
