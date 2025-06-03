/05_anonymity_privacy.md
# Agent Zero - Parrot OS Hacking Prompts
## Phase: 05 - Maintaining Anonymity, Privacy & OpSec (Parrot OS Specifics)

**Objective:** Leverage Parrot OS's built-in and configurable privacy, anonymization, and operational security (OpSec) tools to obscure the source of security testing activities, minimize footprint, and protect attacker infrastructure, when required by the rules of engagement or specific operational needs.

**General Instructions for Agent:**
* These actions typically require `sudo` privileges on the Parrot OS machine. Confirm with the user if not covered by system prompt's auto-confirmation for benign `sudo`, or if explicit confirmation is needed for actions that modify system network state.
* Always verify changes by checking public IP address, DNS resolution, or tool status.
* Log all anonymization and OpSec actions, including status checks before and after changes, to `/work_dir/[project_name]/05_anonymity_ops_log.txt`.
* Understand that some anonymization techniques (especially Tor) can slow down network operations or make certain types of scans (e.g., UDP scans, some Nmap scripts) unreliable or ineffective. Advise the user of these trade-offs.
* Ensure these tools are used in accordance with the engagement's Rules of Engagement (RoE).

---
### Task: Activate System-Wide Tor Routing with Anonsurf
* **Tool(s):** `Anonsurf` (Parrot OS specific integrated tool)
* **Prompt Example:**
    "Activate system-wide Tor routing using Parrot OS's `Anonsurf` to anonymize all network traffic from this machine.
    1.  Execute `sudo anonsurf start`. (Agent: If a password prompt for sudo appears, notify the user. Ideally, passwordless sudo for this specific command is configured if appropriate for the operational context, or the agent can request the password).
    2.  After attempting to start, verify the status robustly using `anonsurf status`.
    3.  Confirm the change in public IP address by querying multiple services: `anonsurf myip`, `curl --silent https://api.ipify.org`, and `curl --silent http://checkip.dyndns.org`.
    Report the Anonsurf status and all reported public IP addresses. Note any discrepancies.
    Save this information (commands, outputs, timestamp) to `/work_dir/[project_name]/05_anonymity_ops_log.txt`."

---
### Task: Stop System-Wide Tor Routing with Anonsurf
* **Tool(s):** `Anonsurf`
* **Prompt Example:**
    "Disable the active system-wide Tor routing provided by `Anonsurf` and revert to the normal network configuration.
    1.  Execute `sudo anonsurf stop`.
    2.  Verify the status using `anonsurf status` to confirm it's stopped.
    3.  Check the current public IP address using multiple methods (e.g., `curl --silent https://api.ipify.org`, `curl --silent http://checkip.dyndns.org`) to ensure it has reverted to the original ISP-assigned IP.
    Report the Anonsurf status and the new (original) public IP address.
    Append this information to `/work_dir/[project_name]/05_anonymity_ops_log.txt`."

---
### Task: Check Anonsurf Status and Current Public IP
* **Tool(s):** `Anonsurf`, `curl` (or similar external IP checking tool like `dig +short myip.opendns.com @resolver1.opendns.com`)
* **Prompt Example:**
    "Provide a comprehensive check of the current `Anonsurf` status and the system's apparent public IP address.
    1.  Execute `anonsurf status` and report its full output.
    2.  Execute `anonsurf myip` and report its output.
    3.  As an independent verification, execute `curl --silent https://api.ipify.org; echo` and `dig +short txt o-o.myaddr.l.google.com @ns1.google.com`.
    Report all outputs clearly. Append to `/work_dir/[project_name]/05_anonymity_ops_log.txt`."

---
### Task: Using `torsocks` or `proxychains` for Specific Commands
* **Tool(s):** `torsocks`, `proxychains4` (Parrot usually has `proxychains-ng` or `proxychains4`), [target command e.g., `curl`, `nmap`, `sqlmap`]
* **Prompt Example (torsocks):**
    "Execute the command `curl -sI http://[target_sensitive_url]` specifically through the Tor network using `torsocks`, without enabling system-wide Anonsurf.
    The command to run is: `torsocks curl -sI http://[target_sensitive_url]`.
    Before running, briefly explain that `torsocks` attempts to redirect TCP connections and DNS lookups from a specific application through Tor.
    Report the output headers. Append command, explanation, and output to `/work_dir/[project_name]/05_anonymity_ops_log.txt`."
* **Prompt Example (proxychains for Nmap - use with extreme caution):**
    "If required by ROE to run an Nmap scan through a proxy chain (e.g., Tor or a custom SOCKS proxy configured in `/etc/proxychains.conf`):
    Prepare the command: `proxychains4 nmap -sT -Pn -p [port1,port2] --max-retries 1 --host-timeout 30s [target_ip]`.
    **State clearly that Nmap over Tor/proxies is generally slow, unreliable, may be incomplete, can put stress on the Tor network, and might be easily detectable by the target as Tor traffic. Confirm with the user if they understand these limitations and wish to proceed with this specific Nmap command via proxychains.**
    If confirmed, execute and report output. Append to `/work_dir/[project_name]/05_anonymity_ops_log.txt`."

---
### Task: MAC Address Spoofing for Network Interface
* **Tool(s):** `macchanger` (GNU MAC Changer)
* **Prompt Example (for interface `eth0`):**
    "If MAC address spoofing is required for the network interface `eth0` (e.g., to bypass MAC filtering on a local network or reduce traceability on public Wi-Fi):
    1.  Display current MAC: `macchanger -s eth0`.
    2.  Bring the interface down: `sudo ip link set dev eth0 down`.
    3.  Use `macchanger` to set a fully random MAC address: `sudo macchanger -A eth0` (or `-r` for a vendor-agnostic random MAC, or `-p` to keep vendor bytes).
    4.  Bring the interface back up: `sudo ip link set dev eth0 up`.
    5.  Verify the new MAC address: `macchanger -s eth0` and `ip link show eth0`.
    **Confirm with the user before executing these steps, as it will temporarily disrupt network connectivity on `eth0` and might require DHCP renewal.**
    Report the original and new MAC addresses. Append actions and outputs to `/work_dir/[project_name]/05_anonymity_ops_log.txt`."
    *(Note: MAC address spoofing effectiveness varies. It's most relevant on local Layer 2 networks. It does not anonymize IP traffic beyond the local gateway.)*

---
### Task: Clearing Command History and Logs (Attacker Machine - Use with Discretion)
* **Tool(s):** `history -c`, `shred`, `rm`
* **Prompt Example (VERY CAUTIONARY - typically for post-engagement cleanup if ROE permits):**
    "If explicitly authorized by the Rules of Engagement for post-engagement cleanup on this Parrot OS attacker machine:
    1.  Clear the current bash session history: `history -c && history -w`.
    2.  Securely delete specific sensitive log files we created (e.g., `/work_dir/[project_name]/sensitive_notes.txt`) using `shred -uzn 3 /work_dir/[project_name]/sensitive_notes.txt`.
    **These actions are destructive to forensic evidence on the attacker machine. Confirm with the user the exact files or history to be cleared and obtain explicit confirmation (e.g., 'USER_CONFIRMS_CLEAR_BASH_HISTORY_AND_SHRED_FILE [filename]') before proceeding.**
    Log the confirmation and action to a separate, secure audit log if one exists for the attacker's actions."
    *(Agent: This is a highly sensitive operation. Emphasize that this is about cleaning the *attacker's* machine, not the target, and only if part of a legitimate, authorized cleanup procedure.)*
