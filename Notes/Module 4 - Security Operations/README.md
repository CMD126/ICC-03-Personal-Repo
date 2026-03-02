# Security Operations Cheat Sheet

A reference for SOC roles, SIEM, incident response, and log analysis.

---

## SOC Overview

| Role | Responsibility |
|------|---------------|
| **SOC Analyst (Tier 1)** | Monitor alerts, perform initial triage, escalate confirmed incidents. |
| **SOC Analyst (Tier 2)** | Deep-dive investigation, threat correlation, malware analysis. |
| **SOC Analyst (Tier 3)** | Advanced threat hunting, forensics, root cause analysis, tool development. |
| **SOC Manager** | Oversee SOC operations, reporting, staffing, and process improvement. |
| **Threat Intelligence Analyst** | Research threat actors, TTPs, and feed intel into detections. |
| **Incident Responder** | Lead response to confirmed security incidents. |

---

## SIEM (Security Information and Event Management)

| Concept | Description |
|---------|-------------|
| **SIEM** | Platform that aggregates, correlates, and analyzes log data from across the environment. |
| **Log Aggregation** | Collecting logs from multiple sources into a central repository. |
| **Correlation Rule** | Logic that triggers an alert when specific event patterns occur. |
| **Use Case** | A defined detection scenario (e.g., brute force, lateral movement). |
| **True Positive (TP)** | Alert correctly identifies a real threat. |
| **False Positive (FP)** | Alert fires but no real threat exists. |
| **True Negative (TN)** | No alert, no threat — correct. |
| **False Negative (FN)** | Threat exists but no alert fired — missed detection. |
| **Baseline** | Normal behavior profile used to detect anomalies. |
| **Retention** | How long log data is stored in the SIEM. |

### Common SIEM Platforms

| Platform | Notes |
|----------|-------|
| **Splunk** | Industry-leading SIEM; uses SPL (Splunk Processing Language). |
| **Microsoft Sentinel** | Cloud-native SIEM on Azure; uses KQL. |
| **IBM QRadar** | Enterprise SIEM with strong correlation capabilities. |
| **Elastic SIEM** | Open-source stack (ELK); flexible and cost-effective. |
| **Chronicle (Google)** | Cloud-scale SIEM by Google; uses YARA-L rules. |

---

## Incident Response Lifecycle (NIST SP 800-61)

| Phase | Description |
|-------|-------------|
| **1. Preparation** | Build tools, train teams, define policies, set up monitoring before an incident occurs. |
| **2. Detection & Analysis** | Identify and validate that an incident has occurred; determine scope and severity. |
| **3. Containment** | Limit the spread of the incident (short-term and long-term containment). |
| **4. Eradication** | Remove the root cause — malware, backdoors, compromised accounts. |
| **5. Recovery** | Restore systems to normal operation and verify integrity. |
| **6. Post-Incident Activity** | Conduct lessons-learned review; update documentation and detections. |

---

## Incident Severity Levels

| Level | Description | Example |
|-------|-------------|---------|
| **P1 / Critical** | Immediate threat to business operations or data. | Active ransomware, data breach in progress |
| **P2 / High** | Significant risk requiring urgent response. | Compromised admin account, C2 detected |
| **P3 / Medium** | Moderate risk; investigate promptly. | Phishing email opened, suspicious login |
| **P4 / Low** | Minimal risk; handle during business hours. | Single failed login, informational alert |

---

## Key Log Sources

| Source | What to Look For |
|--------|-----------------|
| **Windows Event Logs** | Login events (4624, 4625), privilege use (4672), process creation (4688). |
| **Syslog (Linux)** | Auth failures (`/var/log/auth.log`), sudo use, cron jobs. |
| **Firewall Logs** | Blocked/allowed traffic, port scans, unusual outbound connections. |
| **DNS Logs** | DGA domains, DNS tunneling, high-frequency queries. |
| **Web Proxy Logs** | Malicious URLs, data exfiltration via HTTP, user-agent anomalies. |
| **EDR Logs** | Process trees, file writes, registry changes, network connections by process. |

---

## Common Threat Indicators

| Indicator | Description |
|-----------|-------------|
| **IOC** | Indicator of Compromise — evidence a system has been breached (IP, hash, domain). |
| **Brute Force** | Repeated failed logins followed by a success. |
| **Lateral Movement** | Internal traffic between hosts using tools like PsExec, WMI, RDP. |
| **C2 (Command & Control)** | Outbound connections to attacker infrastructure; often beaconing at regular intervals. |
| **Exfiltration** | Large or unusual outbound data transfers. |
| **Persistence** | New scheduled tasks, registry run keys, or services created post-compromise. |
