# Cloud Security Cheat Sheet

A reference for cloud security concepts, shared responsibility, IAM, and common cloud threats.

---

## Cloud Service Models

| Model | Full Name | Description | Examples |
|-------|-----------|-------------|---------|
| **IaaS** | Infrastructure as a Service | Provider manages hardware/network; customer manages OS, apps, data. | AWS EC2, Azure VMs, GCP Compute |
| **PaaS** | Platform as a Service | Provider manages OS and runtime; customer manages apps and data. | AWS Elastic Beanstalk, Azure App Service |
| **SaaS** | Software as a Service | Provider manages everything; customer only manages data and access. | Microsoft 365, Google Workspace, Salesforce |

---

## Shared Responsibility Model

| Responsibility | IaaS | PaaS | SaaS |
|----------------|------|------|------|
| Data & Content | Customer | Customer | Customer |
| Identity & Access | Customer | Customer | Shared |
| Applications | Customer | Customer | Provider |
| Runtime / OS | Customer | Provider | Provider |
| Virtualization | Provider | Provider | Provider |
| Physical Hardware | Provider | Provider | Provider |

> **Rule of thumb:** The higher up the stack, the more the provider manages — but the customer is **always** responsible for their own data and access controls.

---

## Identity and Access Management (IAM)

| Concept | Description |
|---------|-------------|
| **IAM** | Framework of policies and technologies to manage who can access what resources. |
| **Principal** | Any entity that can make a request (user, role, service account). |
| **Policy** | Document defining permissions (allow/deny actions on resources). |
| **Role** | A set of permissions that can be assumed by a principal. |
| **Least Privilege** | Grant only the minimum permissions necessary to perform a task. |
| **MFA** | Multi-Factor Authentication — require a second factor beyond a password. |
| **Service Account** | Non-human identity used by applications and services. |
| **Federation** | Using an external identity provider (IdP) to authenticate (SSO/SAML/OIDC). |

---

## Cloud Security Key Services

| Provider | Service | Purpose |
|----------|---------|---------|
| **AWS** | IAM | User/role/policy management. |
| **AWS** | GuardDuty | Threat detection using ML and logs. |
| **AWS** | CloudTrail | API activity logging and auditing. |
| **AWS** | Security Hub | Centralized security posture management. |
| **AWS** | S3 Bucket Policies | Control access to object storage. |
| **Azure** | Entra ID (AAD) | Identity and access management. |
| **Azure** | Defender for Cloud | Security posture and threat protection. |
| **Azure** | Monitor / Sentinel | Logging, SIEM, and threat detection. |
| **GCP** | IAM | Identity and resource access management. |
| **GCP** | Security Command Center | Centralized security and risk platform. |

---

## Common Cloud Threats

| Threat | Description |
|--------|-------------|
| **Misconfiguration** | Publicly exposed storage buckets, overly permissive IAM roles, open security groups. |
| **Credential Theft** | Stolen API keys, access tokens, or service account credentials. |
| **Insecure APIs** | Unauthenticated or poorly secured cloud API endpoints. |
| **Account Hijacking** | Phishing or credential stuffing to gain access to cloud accounts. |
| **Data Exfiltration** | Unauthorized copying of data to external destinations. |
| **Privilege Escalation** | Abusing overly permissive roles or policies to gain elevated access. |
| **Shadow IT** | Unauthorized cloud services used by employees outside IT oversight. |
| **SSRF** | Server-Side Request Forgery — used to query cloud metadata endpoints (e.g., `169.254.169.254`). |

---

## Cloud Security Best Practices

| Practice | Description |
|----------|-------------|
| **Enable MFA** | Require MFA on all accounts, especially root/admin. |
| **Audit IAM roles** | Regularly review and remove unused permissions. |
| **Encrypt data** | Use provider-managed or customer-managed keys for data at rest and in transit. |
| **Enable logging** | Turn on CloudTrail, Azure Monitor, or GCP Audit Logs. |
| **Lock down storage** | Block public access to S3 buckets and blob storage by default. |
| **Use security groups** | Restrict inbound/outbound traffic to only what's needed. |
| **Monitor for anomalies** | Use GuardDuty, Defender, or SCC to detect unusual behavior. |
