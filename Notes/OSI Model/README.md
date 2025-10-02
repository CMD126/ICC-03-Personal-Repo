# OSI Model Cheat Sheet

The **OSI (Open Systems Interconnection) model** is a 7-layer framework that standardizes how devices communicate over networks.

Mnemonic (top → bottom): **All People Seem To Need Data Processing**  
(Application, Presentation, Session, Transport, Network, Data Link, Physical)

---

| Layer | Name | Function | Examples |
|-------|------|----------|----------|
| **7** | Application | Provides network services directly to end-user applications. Defines protocols for communication. | HTTP, HTTPS, FTP, SMTP, DNS |
| **6** | Presentation | Translates data into a usable format, handles encryption/decryption and compression. | SSL/TLS, JPEG, MPEG, GIF |
| **5** | Session | Manages sessions between applications: establishes, maintains, and terminates connections. | NetBIOS, RPC, PPTP |
| **4** | Transport | Provides reliable delivery, segmentation, sequencing, flow control, and error checking. Defines ports. | TCP, UDP, SCTP |
| **3** | Network | Handles logical addressing, routing, and packet forwarding across networks. | IP (IPv4/IPv6), ICMP, IPsec |
| **2** | Data Link | Provides node-to-node data transfer, framing, and MAC addressing. Error detection. | Ethernet, Wi-Fi (802.11), ARP, PPP |
| **1** | Physical | Transmits raw bits over physical media as electrical, optical, or radio signals. | Cables, hubs, switches, fiber, radio waves |

---

## OSI vs TCP/IP (Comparison)

| OSI Model (7 Layers) | TCP/IP Model (4 Layers) |
|-----------------------|--------------------------|
| Application | Application |
| Presentation | Application |
| Session | Application |
| Transport | Transport |
| Network | Internet |
| Data Link | Network Access |
| Physical | Network Access |
