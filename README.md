# DeceptNet: A Honeypot-Based Threat Detection & Attacker Behavior Analysis Lab
> A honeypot-based threat detection lab built to capture, detect, and analyze attacker behavior using real open-source security tools.

## Architecture

![DeceptNet Architecture](diagram.png)

## Tools Used

| Tool | Role |
|------|------|
| Cowrie | SSH honeypot — captures attacker sessions |
| Suricata | Network IDS — detects scans and suspicious traffic |
| Wazuh | SIEM — correlates alerts, custom detection rules |
| Filebeat | Log shipper — Cowrie logs → Wazuh pipeline |
| Python (pandas, matplotlib) | Attacker behavior analysis and visualization |
| Kali Linux | Attacker simulation machine |
| VirtualBox | Lab virtualization environment |

## Lab Environment

- **Ubuntu Server 22.04** — hosts Cowrie, Suricata, Wazuh Manager + Agent, Filebeat
- **Kali Linux** — attacker machine
- **VirtualBox** — Host-Only networking between VMs

## What It Does

- Lures attackers into a fake SSH server (Cowrie)
- Detects network scanning with custom Suricata rules
- Ships all logs to Wazuh via Filebeat
- Fires real-time alerts using custom Wazuh detection rules
- Analyzes attacker behavior and generates visual reports with Python

## Custom Wazuh Rules

| Rule ID | Event | ATT&CK Technique | ID |
|---|---|---|---|
| 100101 | Cowrie login success | Valid Accounts | T1078 |
| 100102 | Cowrie command input | Command and Scripting Interpreter: Unix Shell | T1059.004 |
| 100103 | Cowrie session connect | ( this is just connection, not really an ATT&CK technique on its own) |

## Simulations

### 1. Brute-Force Attack
- **Tool:** Hydra
- **Target:** Cowrie SSH honeypot (port 2222)
- **Result:** 61 failed attempts, credential `root/admin123` discovered

![Login Success vs Failed](docs/login-success-vs-failed-chart.png)

### 2. Post-Compromise Session
After a successful login, the attacker ran recon commands inside the honeypot:

`whoami` `uname -a` `id` `cat /etc/passwd` `ls -la /root` `ps aux` `netstat -antp` `wget` `history`

All commands captured as `cowrie.command.input` events in Wazuh.

![Wazuh Alerts Overview](docs/wazuh_discover_cowrie_alerts_overview.png)

## Attacker Behavior Analysis

Using Python (pandas + matplotlib), Cowrie's JSON logs were parsed to:
- Count login attempts (success vs failure)
- Extract and frequency-rank every command executed post-compromise
- Identify attacker recon patterns: system enumeration → process listing → network recon → exfiltration attempt

## Key Findings

- Attacker used credential stuffing — 61 attempts before finding working credential
- Post-compromise behavior followed a classic recon pattern
- `wget` to external domain flagged as exfiltration attempt

## screenshots
### Wazuh Custom Rule 100101 — Cowrie Login Success Detected
![Custom Rule 100101](docs/wazuh-custom-rule-100101-cowrie-login-success.png)
*Custom Wazuh rule 100101 firing on successful honeypot login — root/admin123*

### Wazuh Discover — Cowrie Login Success Event
![Wazuh Login Success](docs/wazuh-discover-cowrie-login-success.png)
*Wazuh Discover showing cowrie.login.success event from Kali attacker machine*

### Wazuh — Suricata SYN Scan Detection
![Suricata Detection](docs/wazuh_suricata_syn_scan_detection.png)
*Custom Suricata rule sid:1000001 detecting SYN scan — alert visible in Wazuh*

### Python Analysis Output
![Python Analysis](docs/python-login-analysis-summary.png)
*Python script parsing Cowrie logs — 360 events, 61 failed logins, top usernames and passwords*
