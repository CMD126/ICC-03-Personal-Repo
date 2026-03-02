# Data Security Cheat Sheet

A reference for encryption, data classification, data loss prevention, and secure data handling.

---

## Encryption Types

| Type | Description | Examples |
|------|-------------|---------|
| **Symmetric** | Same key used to encrypt and decrypt. Fast, but key distribution is a challenge. | AES, DES, 3DES, RC4 |
| **Asymmetric** | Public key encrypts, private key decrypts (or vice versa). Slower but solves key distribution. | RSA, ECC, Diffie-Hellman |
| **Hashing** | One-way transformation — produces a fixed-length digest. Not reversible. | MD5, SHA-1, SHA-256, bcrypt |
| **Hybrid** | Combines symmetric and asymmetric (asymmetric exchanges a symmetric key). | TLS/HTTPS, PGP |

---

## Encryption Key Terms

| Term | Description |
|------|-------------|
| **Plaintext** | Original, unencrypted data. |
| **Ciphertext** | Data after encryption. |
| **Key** | A value used by an algorithm to encrypt or decrypt data. |
| **IV (Initialization Vector)** | Random value added to encryption to ensure identical plaintexts produce different ciphertexts. |
| **Salt** | Random data added to a password before hashing to prevent rainbow table attacks. |
| **PKI** | Public Key Infrastructure — system for managing digital certificates and public key encryption. |
| **Certificate** | Digital document binding a public key to an identity, signed by a CA. |
| **CA** | Certificate Authority — trusted entity that issues digital certificates. |

---

## Data Classification

| Level | Description | Examples |
|-------|-------------|---------|
| **Public** | No harm if disclosed; freely shareable. | Marketing material, press releases |
| **Internal** | Low sensitivity; intended for internal use only. | Internal policies, org charts |
| **Confidential** | Sensitive; limited to authorized personnel. | Business plans, financial data |
| **Restricted / Top Secret** | Highest sensitivity; could cause severe damage if disclosed. | PII, PHI, trade secrets, credentials |

---

## Data States

| State | Description | Protection Methods |
|-------|-------------|-------------------|
| **Data at Rest** | Stored data (disk, database, backup). | Full-disk encryption (FDE), AES, BitLocker |
| **Data in Transit** | Data moving across a network. | TLS, VPN, HTTPS, SFTP |
| **Data in Use** | Data actively being processed in memory. | Secure enclaves, memory encryption (e.g., AMD SME) |

---

## Data Loss Prevention (DLP)

| Concept | Description |
|---------|-------------|
| **DLP** | Technology and policies to detect and prevent unauthorized data exfiltration. |
| **Endpoint DLP** | Monitors and controls data on devices (USB, email, print). |
| **Network DLP** | Inspects data in transit across the network. |
| **Cloud DLP** | Protects data stored or shared in cloud services. |
| **Content Inspection** | Scanning data for sensitive patterns (SSNs, credit cards, keywords). |
| **Data Masking** | Replacing sensitive data with realistic but fake values (for testing). |
| **Tokenization** | Replacing sensitive data with non-sensitive tokens; original data stored separately. |
| **Redaction** | Permanently removing or obscuring sensitive information. |

---

## Backup & Recovery

| Term | Description |
|------|-------------|
| **Full Backup** | Complete copy of all data. Slowest to back up, fastest to restore. |
| **Incremental Backup** | Only changes since the last backup. Fastest to back up, slowest to restore. |
| **Differential Backup** | Changes since the last full backup. Moderate speed for both backup and restore. |
| **3-2-1 Rule** | Keep **3** copies of data, on **2** different media types, with **1** offsite copy. |
| **RTO** | Recovery Time Objective — how quickly systems must be restored. |
| **RPO** | Recovery Point Objective — how much data loss is acceptable (measured in time). |
| **Snapshot** | Point-in-time copy of data, often used in virtual environments. |
