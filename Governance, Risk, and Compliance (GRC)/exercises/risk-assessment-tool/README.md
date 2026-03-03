# Risk Assessment Tool

Hands-on exercise for understanding GRC risk management: building a risk register, scoring risks using Likelihood × Impact, and selecting appropriate response strategies.

---

## What You Will Learn

- How to identify and document risks (asset, threat, vulnerability)
- Risk scoring using the Likelihood × Impact formula
- Severity levels: Low, Medium, High, Critical
- Risk response strategies: Accept, Mitigate, Transfer, Avoid
- How to read and use a 5×5 risk matrix
- What a risk register looks like in practice

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Add Risk | Enter asset, threat, vulnerability, likelihood (1–5), and impact (1–5). Score is auto-calculated. |
| 2 | View Register | Table of all risks sorted by score (highest first) with severity and status |
| 3 | View Risk Detail | Full breakdown of a single risk entry |
| 4 | Risk Matrix | 5×5 scoring matrix with severity zones and response guidance |

---

## Usage

```bash
python3 risk_assessment_tool.py
```

Risk entries are saved to `risk_register.json` in the same directory and reloaded on the next run.

---

## Requirements

Pure Python 3 stdlib — no external packages needed.

| Module | Used for |
|--------|----------|
| `json` | Saving and loading the risk register |
| `os` | File existence checks |

---

## Risk Scoring Reference

| Score | Severity | Response |
|-------|----------|---------|
| 1–4 | Low | Accept — monitor periodically |
| 5–9 | Medium | Mitigate within 90 days |
| 10–14 | High | Mitigate within 30 days |
| 15–25 | Critical | Immediate escalation required |
