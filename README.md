<div align="center">

# 🛡️ DAEMON — Attack Surface Mapping & Recon Suite

**Dynamic Assessment & Endpoint Mapping Orchestration Network**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kali Linux](https://img.shields.io/badge/OS-Kali%20Linux-555555?style=for-the-badge&logo=kalilinux&logoColor=white)
![Nmap](https://img.shields.io/badge/Engine-Nmap-008080?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*An automated Python framework for rapid network reconnaissance, targeted port auditing, and infrastructure discovery.*

</div>

---

## 📌 Overview

**DAEMON** is a lightweight, high-speed reconnaissance automation tool designed to streamline initial penetration testing workflows. Instead of manually running standalone terminal commands, DAEMON orchestrates network discovery and DNS resolution into a unified execution pipeline, automatically exporting detailed technical telemetry into structured PDF documentation.

---

## ⚙️ Core Features & Capabilities

- 🎯 **Automated Port Audit:** Executes targeted TCP port scanning (`21, 22, 25, 53, 80, 443`) using native `Nmap` sub-processes.
- 🖥️ **OS & Service Versioning:** Fingerprints remote service versions and underlying OS parameters.
- 🌐 **DNS & Domain Reconnaissance:** Resolves target hostname infrastructure and name server records via `nslookup`.
- 📄 **Executive PDF Reporting:** Automatically compiles raw terminal logs into structured audit reports using `ReportLab`.
- ⚡ **Zero External Heavy Dependencies:** Pure Python standard library automation interfacing directly with Linux native utilities.

---

## 🏗️ Technical Architecture


```

```
             +-----------------------+
             |   User Target Input   |
             +-----------+-----------+
                         |
                         v
             +-----------------------+
             |    DAEMON Engine      |
             +-----+-----------+-----+
                   |           |
    +--------------+           +--------------+
    |                                         |
    v                                         v

```

+---------------+                         +---------------+
|  Nmap Module  |                         |  DNS Module   |
| (Ports/OS/v)  |                         |  (nslookup)   |
+-------+-------+                         +-------+-------+
|                                         |
+--------------+-----------+--------------+
|
v
+--------------------+
| PDF Audit Report   |
|   (ReportLab)      |
+--------------------+

```

---

## 🚀 Installation & Getting Started

### 1. System Requirements
Ensure your Linux system (Kali Linux recommended) has Python 3, Git, and Nmap installed:

```bash
sudo apt update && sudo apt install git python3 python3-pip nmap -y

```

### 2. Python Dependencies

Install the required PDF generation library:

```bash
pip install reportlab

```

### 3. Clone Repository

```bash
git clone [https://github.com/Anas-Abdullah-Sec/DAEMON.git](https://github.com/Anas-Abdullah-Sec/DAEMON.git)
cd DAEMON

```

---

## 💻 Usage

Run the main CLI script:

```bash
python3 daemon.py

```

1. Enter your target IP or Domain when prompted (e.g., `scanme.nmap.org`).
2. The interactive terminal script will execute Nmap and DNS reconnaissance.
3. Your formatted PDF audit report will be saved automatically in the local directory.

---

## 📝 Example Output

Upon completion, DAEMON generates an executive report containing:

* Target Metadata & Timestamp
* Open Ports & Service Version Matrix
* DNS Mapping Details

---

⚠️ Disclaimer
This tool is intended strictly for educational purposes and authorized security auditing. Usage of DAEMON against target systems without explicit prior consent is illegal. The author accepts no responsibility for unauthorized or malicious use.

📜 License
Distributed under the MIT License. See LICENSE for more information.

👨‍💻 Author
Anas Abdullah

Cybersecurity Enthusiast

🌐 GitHub: @Anas-Abdullah-Sec

💼 LinkedIn: Anas Abdullah
