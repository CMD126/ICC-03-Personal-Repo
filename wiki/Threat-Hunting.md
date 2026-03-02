# Threat Hunting

Proactive threat detection using MITRE ATT&CK, threat intelligence, and behavioral analysis.

---

## Notes

### Threat Hunting Process

| Phase | Description |
|-------|-------------|
| Hypothesis | Form a theory based on intel or anomaly (e.g., "attacker is using living-off-the-land binaries") |
| Data Collection | Pull logs from SIEM, EDR, network sensors |
| Investigation | Query, filter, correlate, visualize |
| Discovery | Confirm or rule out the hypothesis |
| Response | Escalate to IR if threat confirmed; document findings |

### MITRE ATT&CK Tactics (Enterprise)

| ID | Tactic | Goal |
|----|--------|------|
| TA0001 | Initial Access | Get into the network |
| TA0002 | Execution | Run malicious code |
| TA0003 | Persistence | Maintain foothold |
| TA0004 | Privilege Escalation | Gain higher access |
| TA0005 | Defense Evasion | Avoid detection |
| TA0006 | Credential Access | Steal credentials |
| TA0007 | Discovery | Learn the environment |
| TA0008 | Lateral Movement | Move through the network |
| TA0009 | Collection | Gather target data |
| TA0010 | Exfiltration | Send data out |
| TA0011 | Command & Control | Communicate with attacker |
| TA0040 | Impact | Disrupt, destroy, encrypt |

### Pyramid of Pain

| Level | Indicator | Difficulty to change |
|-------|-----------|---------------------|
| Hash values | IOC | Trivial |
| IP addresses | IOC | Easy |
| Domain names | IOC | Simple |
| Network artifacts | TTP | Annoying |
| Host artifacts | TTP | Annoying |
| Tools | TTP | Challenging |
| TTPs | Behavior | Tough |

→ [View full cheat sheet](../Threat%20Hunting/notes/README.md)

---

## Exercises

Exercises in progress.

---

[← Home](Home)
