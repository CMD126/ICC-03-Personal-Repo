#!/usr/bin/env python3
"""
IAM Policy Analyzer — Educational Exercise
Demonstrates cloud security concepts: IAM policy structure,
least privilege principle, and common misconfiguration patterns.
"""

import json
import os
import sys

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║           IAM POLICY ANALYZER — Educational                 ║
║    Least Privilege · Wildcards · Misconfigurations          ║
╚══════════════════════════════════════════════════════════════╝
"""

DANGEROUS_ACTIONS = {
    "*":            ("CRITICAL", "Full access to ALL services"),
    "iam:*":        ("CRITICAL", "Full IAM control — can create admin users"),
    "s3:*":         ("HIGH",     "Full S3 access — can read/delete all buckets"),
    "ec2:*":        ("HIGH",     "Full EC2 access — can launch/terminate instances"),
    "lambda:*":     ("HIGH",     "Full Lambda access — can execute arbitrary code"),
    "sts:*":        ("HIGH",     "Full STS access — can assume any role"),
    "iam:CreateUser":          ("HIGH",   "Can create new IAM users"),
    "iam:AttachUserPolicy":    ("HIGH",   "Can attach policies to users"),
    "iam:CreateAccessKey":     ("HIGH",   "Can create access keys"),
    "iam:PassRole":            ("MEDIUM", "Can pass roles to services"),
    "s3:GetObject":            ("LOW",    "Read S3 objects"),
    "s3:PutObject":            ("MEDIUM", "Write to S3 buckets"),
    "s3:DeleteObject":         ("MEDIUM", "Delete S3 objects"),
    "sts:AssumeRole":          ("MEDIUM", "Can assume other roles"),
}

def load_policy(path):
    """Load and parse a JSON policy file."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[!] File not found: {path}")
    except json.JSONDecodeError as e:
        print(f"[!] Invalid JSON: {e}")
    return None

def analyze_statement(stmt, idx):
    """Analyze a single policy statement for issues."""
    findings = []
    sid    = stmt.get("Sid", f"Statement-{idx}")
    effect = stmt.get("Effect", "Allow")
    principal = stmt.get("Principal", "N/A")
    actions   = stmt.get("Action", [])
    resource  = stmt.get("Resource", "N/A")

    if isinstance(actions, str):
        actions = [actions]

    # Check for wildcard principal
    if principal == "*" or principal == {"AWS": "*"}:
        findings.append(("CRITICAL", "Principal is '*' — allows ANY entity (public access)"))

    # Check for wildcard resource
    if resource == "*":
        findings.append(("HIGH", "Resource is '*' — applies to ALL resources in account"))

    # Check actions
    action_findings = []
    for action in actions:
        if action in DANGEROUS_ACTIONS:
            sev, desc = DANGEROUS_ACTIONS[action]
            action_findings.append((sev, f"Action '{action}': {desc}"))
        elif action.endswith(":*") and action != "*":
            action_findings.append(("HIGH", f"Action '{action}': wildcard on service"))

    findings.extend(action_findings)

    return sid, effect, principal, actions, resource, findings

def analyze_policy():
    """Analyze an IAM policy file."""
    print("\n  [*] IAM Policy Analyzer\n")
    path = input("[?] Path to policy JSON [default: sample_policy.json]: ").strip()
    if not path:
        path = os.path.join(os.path.dirname(__file__), "sample_policy.json")

    policy = load_policy(path)
    if not policy:
        return

    statements = policy.get("Statement", [])
    if not statements:
        print("[!] No statements found in policy.")
        return

    print(f"\n  Policy Version  : {policy.get('Version', 'N/A')}")
    print(f"  Total Statements: {len(statements)}\n")
    print(f"  {'─'*65}")

    total_issues = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    results = []

    for i, stmt in enumerate(statements, 1):
        sid, effect, principal, actions, resource, findings = analyze_statement(stmt, i)

        status = "PASS" if not findings else ("CRITICAL" if any(s == "CRITICAL" for s, _ in findings) else "WARN")
        results.append((sid, effect, status, findings))

        print(f"\n  Statement #{i}: {sid}")
        print(f"  Effect    : {effect}")
        print(f"  Principal : {json.dumps(principal) if isinstance(principal, dict) else principal}")
        print(f"  Actions   : {', '.join(actions[:3])}{'...' if len(actions) > 3 else ''}")
        print(f"  Resource  : {resource}")

        if findings:
            print(f"  Findings  :")
            for sev, msg in findings:
                marker = "[!!]" if sev == "CRITICAL" else "[! ]" if sev == "HIGH" else "[ *]"
                print(f"    {marker} {sev}: {msg}")
                total_issues[sev] = total_issues.get(sev, 0) + 1
        else:
            print("  Findings  : [OK] No issues detected")

        print(f"  {'─'*65}")

    # Summary
    print(f"""
  ┌─────────────────────────────────────────────────────┐
  │  Analysis Summary                                   │
  └─────────────────────────────────────────────────────┘
  Statements analyzed : {len(statements)}
  CRITICAL issues     : {total_issues['CRITICAL']}
  HIGH issues         : {total_issues['HIGH']}
  MEDIUM issues       : {total_issues['MEDIUM']}
  LOW issues          : {total_issues['LOW']}

  Remediation Tips:
  - Replace Action: '*' with specific required actions only
  - Replace Principal: '*' with specific IAM ARNs
  - Replace Resource: '*' with specific resource ARNs
  - Apply least privilege: grant minimum permissions needed
  - Review IAM permissions quarterly
""")

def explain_iam():
    """Explain IAM policy structure interactively."""
    print("""
  ┌─────────────────────────────────────────────────────┐
  │  IAM Policy Structure Guide                         │
  └─────────────────────────────────────────────────────┘

  A policy is a JSON document with one or more Statements.
  Each Statement has:

    Version    : "2012-10-17" (always use this)
    Statement  : list of permission rules, each containing:
      Sid        : optional identifier for the statement
      Effect     : "Allow" or "Deny"
      Principal  : WHO gets the permission
                   "*" = anyone (dangerous!)
                   "AWS": "arn:aws:iam::123:user/alice"
      Action     : WHAT they can do
                   "*" = everything (very dangerous!)
                   "s3:GetObject" = specific action
      Resource   : ON WHAT (which AWS resource)
                   "*" = all resources (dangerous!)
                   "arn:aws:s3:::my-bucket/*" = specific bucket

  Least Privilege Principle:
    Grant only the minimum permissions required to perform a task.
    Review and remove unused permissions regularly.

  Common Misconfigurations:
    1. Action: '*'          — over-permissive (full access)
    2. Principal: '*'       — public access to resource
    3. Resource: '*'        — applies to all resources
    4. iam:* permissions    — can escalate to admin
    5. No Condition block   — missing MFA/IP restrictions
""")

def main():
    print(BANNER)
    while True:
        print("  Options:")
        print("  1. Analyze an IAM policy file")
        print("  2. Learn IAM policy structure")
        print("  0. Exit\n")
        choice = input("[?] Select option: ").strip()
        print()
        if   choice == "1": analyze_policy()
        elif choice == "2": explain_iam()
        elif choice == "0": print("[+] Goodbye.\n"); sys.exit(0)
        else: print("[!] Invalid option.")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted.\n")
        sys.exit(0)
