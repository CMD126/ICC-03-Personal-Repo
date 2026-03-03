# IAM Policy Analyzer

Hands-on exercise for understanding cloud IAM policy structure, the least privilege principle, and common misconfiguration patterns that lead to privilege escalation and data breaches.

---

## What You Will Learn

- How AWS IAM policy JSON is structured (Version, Statement, Effect, Principal, Action, Resource)
- What the least privilege principle means and why it matters
- How wildcard permissions (`Action: *`, `Principal: *`, `Resource: *`) create security risks
- Common misconfigurations that lead to privilege escalation
- How to read and audit a policy for dangerous permissions

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Analyze Policy File | Parses any JSON IAM policy, flags dangerous permissions per statement, and generates a summary report |
| 2 | Learn IAM Structure | Interactive guide to IAM policy syntax, principal types, action format, and least privilege |

---

## Usage

```bash
python3 iam_policy_analyzer.py
```

Run against the included sample (which has intentional misconfigurations):
```
[?] Path to policy JSON: sample_policy.json
```

---

## Sample Policy

`sample_policy.json` contains 5 statements with deliberate issues:
- A fully open `Action: *` + `Principal: *` + `Resource: *` statement
- A safe read-only S3 statement (baseline for comparison)
- A wildcard EC2 action
- A safe CloudWatch Logs read statement
- An IAM full-access statement (privilege escalation risk)

---

## Requirements

Pure Python 3 stdlib — no external packages needed.

| Module | Used for |
|--------|----------|
| `json` | Parsing IAM policy files |
| `os` | File path handling |
