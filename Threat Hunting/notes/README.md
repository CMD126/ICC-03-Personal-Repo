# Threat Hunting Cheat Sheet

A reference for threat hunting methodology, MITRE ATT&CK, threat intelligence, and key indicators.

---

## What is Threat Hunting?

Threat hunting is the **proactive** search for threats that have evaded automated detections. Unlike reactive alert triage, hunters develop hypotheses and actively look for evidence of adversary activity.

---

## Threat Hunting Process

| Step | Description |
|------|-------------|
| **1. Hypothesis** | Form a hypothesis based on threat intel, ATT&CK TTPs, or anomaly data (e.g., "An attacker is using living-off-the-land techniques to move laterally"). |
| **2. Data Collection** | Identify the log sources and data needed to test the hypothesis. |
| **3. Investigation** | Query and analyze data for indicators supporting or refuting the hypothesis. |
| **4. Pattern Discovery** | Identify malicious patterns, new IOCs, or gaps in detection coverage. |
| **5. Response & Documentation** | Escalate confirmed findings; document the hunt for future automation. |
| **6. Detection Improvement** | Convert successful hunt patterns into new SIEM rules or detections. |

---

## MITRE ATT&CK Framework

| Concept | Description |
|---------|-------------|
| **ATT&CK** | Adversarial Tactics, Techniques, and Common Knowledge — a globally-accessible knowledge base of adversary behavior. |
| **Tactic** | The adversary's goal (the "why") — e.g., Initial Access, Persistence, Exfiltration. |
| **Technique** | How the adversary achieves the tactic (the "how") — e.g., Spearphishing (T1566). |
| **Sub-technique** | A more specific implementation of a technique. |
| **Procedure** | A specific real-world example of a technique used by a threat actor. |
| **Mitigation** | Recommended actions to prevent a technique. |
| **Detection** | Data sources and methods to identify a technique in use. |

### ATT&CK Tactics (in order)

| # | Tactic | Description |
|---|--------|-------------|
| TA0043 | Reconnaissance | Gathering info before the attack. |
| TA0042 | Resource Development | Acquiring infrastructure, tools, or accounts. |
| TA0001 | Initial Access | Getting into the target environment. |
| TA0002 | Execution | Running malicious code. |
| TA0003 | Persistence | Maintaining a foothold. |
| TA0004 | Privilege Escalation | Gaining higher-level permissions. |
| TA0005 | Defense Evasion | Avoiding detection. |
| TA0006 | Credential Access | Stealing credentials. |
| TA0007 | Discovery | Learning about the environment. |
| TA0008 | Lateral Movement | Moving through the network. |
| TA0009 | Collection | Gathering data of interest. |
| TA0011 | Command & Control | Communicating with compromised systems. |
| TA0010 | Exfiltration | Stealing data out of the environment. |
| TA0040 | Impact | Disrupting, destroying, or manipulating systems/data. |

---

## Threat Intelligence

| Term | Description |
|------|-------------|
| **Threat Intelligence** | Evidence-based knowledge about existing or emerging threats used to inform decisions. |
| **Strategic Intel** | High-level trends and adversary motivations for executives and leadership. |
| **Operational Intel** | Information about specific campaigns or attacks in progress. |
| **Tactical Intel** | TTPs used by adversaries — guides detections and hunting. |
| **Technical Intel** | Specific IOCs (IPs, hashes, domains) for blocking and detection. |
| **Threat Actor** | A person or group responsible for malicious activity. |
| **APT** | Advanced Persistent Threat — sophisticated, long-term adversary (often nation-state). |
| **TTP** | Tactics, Techniques, and Procedures — characterizes adversary behavior. |
| **ISAC** | Information Sharing and Analysis Center — sector-specific threat intel sharing group. |

---

## IOCs vs TTPs

| Type | Description | Longevity |
|------|-------------|-----------|
| **Hash** | File hash of malware sample. | Very short — changes with any file modification. |
| **IP Address** | Attacker-controlled IP. | Short — rotated frequently. |
| **Domain** | C2 or phishing domain. | Short-to-medium — can be sinkholed or abandoned. |
| **Network Artifact** | URL pattern, user-agent, protocol behavior. | Medium. |
| **Host Artifact** | Registry keys, file paths, mutexes. | Medium. |
| **TTP** | How the attacker operates (ATT&CK techniques). | Long — hardest for adversaries to change. |

> Based on the **Pyramid of Pain** (David Bianco) — higher on the pyramid = more pain for the adversary when detected.

---

## Common Hunting Data Sources

| Source | What to Hunt |
|--------|-------------|
| **Process Creation Logs** | Unusual parent-child process relationships, LOLBins (living-off-the-land binaries). |
| **Network Logs** | Beaconing traffic, unusual ports, DNS tunneling, TLS to unknown IPs. |
| **Authentication Logs** | Pass-the-hash, Kerberoasting, unusual login times/locations. |
| **PowerShell / Script Logs** | Encoded commands, download cradles, AMSI bypass attempts. |
| **Registry Logs** | Run keys, service modifications, persistence mechanisms. |
| **File System Logs** | Dropped payloads, renamed system binaries, staging directories. |
