# Security Policy

---

## Responsible Use

This repository contains educational cybersecurity tools and simulations. All content is intended strictly for:

- Learning in controlled environments
- Authorized penetration testing
- CTF (Capture the Flag) competitions
- Personal lab environments you own

**Never use these tools against systems you do not own or have explicit written permission to test. Unauthorized scanning or exploitation may be illegal in your jurisdiction.**

---

## Sensitive Scripts

| Script | Risk Level | Requirement |
|--------|-----------|-------------|
| `ransomware-simulator` | High | Run only in an isolated VM — never on a real system |
| `recon-tool` | Medium | Only target domains/IPs you own or have permission to scan |
| `nmatrix` / `network-tool` | Low-Medium | Avoid scanning external targets without authorization |
| `port-scanner` | Medium | Only test systems you have explicit permission to scan |

---

## Reporting a Vulnerability

If you find a security issue in this repository (e.g., a script that could cause unintended harm):

1. **Do not open a public GitHub issue**
2. Contact the repository owner directly via GitHub
3. Provide a clear description of the issue and potential impact

---

→ [View full SECURITY.md](../SECURITY.md) | [← Home](Home)
