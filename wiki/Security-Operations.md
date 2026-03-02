# Security Operations

SOC workflows, SIEM, incident response, and log analysis.

---

## Notes

### SOC Roles

| Role | Responsibilities |
|------|----------------|
| Tier 1 Analyst | Alert triage, initial investigation |
| Tier 2 Analyst | Deep-dive analysis, escalations |
| Tier 3 / IR | Incident response, threat hunting |
| SOC Manager | Operations oversight, metrics |

### Incident Response Lifecycle

| Phase | Actions |
|-------|---------|
| Preparation | Policies, playbooks, tools |
| Identification | Detect and confirm the incident |
| Containment | Isolate affected systems |
| Eradication | Remove malware, close vulnerabilities |
| Recovery | Restore systems, verify clean |
| Lessons Learned | Post-incident review, documentation |

### Alert Severity Levels

| Level | Response |
|-------|---------|
| Critical | Immediate response — active breach |
| High | Respond within 1 hour |
| Medium | Respond within 24 hours |
| Low | Review within 72 hours |
| Informational | Log only |

### Common Log Sources

| Source | What it shows |
|--------|--------------|
| `/var/log/auth.log` | SSH logins, sudo, PAM events |
| `/var/log/syslog` | General system events |
| Windows Event Log | Logins (4624), failures (4625), process creation (4688) |
| Firewall logs | Allow/deny decisions, port traffic |
| Web server logs | HTTP requests, status codes, IPs |

→ [View full cheat sheet](../Security%20Operations/notes/README.md)

---

## Exercises

### log-analyzer
Parses SSH `auth.log` to detect security events.
- Brute force detection (threshold: 5 failed attempts from same IP)
- Tracks successful logins
- Detects invalid username enumeration
- Outputs a formatted SOC-style security report

→ [View exercise](../Security%20Operations/exercises/log-analyzer/)

---

[← Home](Home)
