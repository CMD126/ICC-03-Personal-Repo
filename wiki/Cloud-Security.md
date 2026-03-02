# Cloud Security

Cloud service models, shared responsibility, IAM, and cloud-specific threats.

---

## Notes

### Service Models

| Model | Provider manages | Customer manages |
|-------|-----------------|-----------------|
| IaaS | Hardware, networking, virtualization | OS, middleware, apps, data |
| PaaS | IaaS + OS + runtime | Apps and data |
| SaaS | Everything | Data and access |

### Shared Responsibility Model

| Layer | IaaS | PaaS | SaaS |
|-------|------|------|------|
| Data | Customer | Customer | Customer |
| Application | Customer | Customer | Provider |
| Runtime | Customer | Provider | Provider |
| OS | Customer | Provider | Provider |
| Infrastructure | Provider | Provider | Provider |

### IAM Key Concepts

| Concept | Description |
|---------|-------------|
| Principal | User, role, or service requesting access |
| Policy | JSON document defining allowed/denied actions |
| Role | Temporary identity assumed by a service or user |
| MFA | Multi-factor authentication — always enable on root/admin |
| Least Privilege | Grant only the minimum permissions needed |

### Cloud Threats

| Threat | Description |
|--------|-------------|
| Misconfiguration | Open S3 buckets, public databases, exposed APIs |
| Credential theft | Leaked keys in code, metadata endpoint abuse |
| Privilege escalation | Overly permissive IAM roles |
| Insecure APIs | Unauthenticated endpoints, broken object auth |
| Data exfiltration | Unmonitored egress, misconfigured storage |

→ [View full cheat sheet](../Cloud%20Security/notes/README.md)

---

## Exercises

Exercises in progress.

---

[← Home](Home)
