quick_host_recon_instrument_def.md
# Agent Zero - Parrot OS Hacking Prompts
## Instrument Definition: QuickHostRecon

**Objective:** Define a reusable Agent Zero instrument for performing a quick, initial reconnaissance scan on a single target IP address to determine its status and common open ports. This instrument is designed for speed and initial assessment.

**Instrument Name:** `QuickHostRecon`

**Argument(s):**
* `target_ip`: (String) The IP address of the target host. (e.g., "192.168.1.100")
* `output_tag`: (String, Optional) A tag to include in the output filename for better organization. (e.g., "dmz_server")

**Sequence of Actions (using Parrot OS tools):**

1.  **ICMP Ping Check (Host Responsiveness):**
    * **Tool:** `ping`
    * **Command:** `ping -c 4 -W 1 [target_ip]` (Send 4 packets, 1-second timeout per packet)
    * **Purpose:** Quickly determine if the host is responsive to ICMP echo requests.
    * **Output Handling:** Report if the host is "UP" (received replies) or "DOWN" (no replies). Note packet loss if any.

2.  **Fast TCP Port Scan (Common Ports):**
    * **Tool:** `nmap`
    * **Command:** `nmap -F --reason -T4 [target_ip]` (Fast scan of Nmap's default top 100 ports, show reason for port state, aggressive timing)
    * **Purpose:** Quickly identify the most common open TCP ports and their associated services. `--reason` helps understand why Nmap determined a port's state.
    * **Output Handling:** Report all open TCP ports, their states (e.g., open, open|filtered), and the identified services.

3.  **(Optional) UDP Port Scan (Very Common Ports - if specified):**
    * **Conditional Execution:** Only if an additional argument `check_udp` is set to `true` during instrument call (or make it a separate instrument).
    * **Tool:** `nmap`
    * **Command:** `sudo nmap -sU --top-ports 20 --reason -T4 [target_ip]` (Scan top 20 UDP ports, requires sudo)
    * **Purpose:** Check for very common open UDP services (DNS, NTP, SNMP etc.). UDP scans are slower and less reliable.
    * **Output Handling:** Report open UDP ports, states, and services. Advise that UDP scan results can be less reliable.

**Storage and Reporting:**

* All raw outputs from `ping` and `nmap` for this instrument run should be concatenated and saved to a uniquely named file within `/work_dir/instruments_output/QuickHostRecon/`.
* The filename should incorporate the target IP and the optional output tag:
    `qhr_[target_ip]_[output_tag_if_provided]_[timestamp].log`
    (Example: `qhr_192.168.1.100_dmz_server_202406031030.log`)
* A concise summary of findings should be provided to the user upon completion, including:
    * Target IP Address.
    * Ping Status (UP/DOWN, packet loss).
    * List of Open TCP Ports: Port Number, Protocol, Service Name, Reason.
    * (If UDP scanned) List of Open UDP Ports: Port Number, Protocol, Service Name, Reason.

**Prompt to Define this Instrument with Agent Zero:**
"Use the instrument 'QuickHostRecon' with the following arguments:
target_ip: '[specific_target_ip]'
output_tag: 'webserver_check'

Ensure all outputs are logged as per the instrument's definition.
Report the summary back to me."
