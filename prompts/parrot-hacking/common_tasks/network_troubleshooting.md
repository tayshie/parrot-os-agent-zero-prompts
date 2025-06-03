network_troubleshooting.md
# Agent Zero - Parrot OS Hacking Prompts
## Common Task: Basic Network Troubleshooting (Attacker Machine)

**Objective:** Perform basic network connectivity checks and diagnostics from the Parrot OS machine where Agent Zero is operating. This is for troubleshooting the agent's own connectivity or reachability to targets.

**General Instructions for Agent:**
* These commands are typically run on the Parrot OS host itself.
* Use standard Linux networking utilities (`ping`, `ip`, `ss`, `netstat`, `host`, `dig`, `curl`, `traceroute`).
* Interpret results to diagnose common issues like no connectivity, DNS problems, or blocked ports.

---
### Task: Check Basic Connectivity to a Host
* **Tool(s):** `ping`
* **Prompt Example:**
    "Check if the host `192.168.1.100` is reachable by sending 5 ICMP echo requests. Report packet loss and average round-trip time."
    * **Agent Action Example:** `ping -c 5 192.168.1.100`

---
### Task: Check Local IP Configuration
* **Tool(s):** `ip addr show`, `ifconfig` (if `ip` is not preferred)
* **Prompt Example:**
    "Display the current IP address, netmask, and gateway for all active network interfaces on this Parrot OS machine."
    * **Agent Action Example:** `ip addr show` (and potentially `ip route show` for gateway)

---
### Task: Check Listening Ports on Local Machine
* **Tool(s):** `ss`, `netstat`
* **Prompt Example:**
    "List all TCP and UDP ports that this Parrot OS machine is currently listening on, along with the processes associated with them. Do not resolve hostnames."
    * **Agent Action Example:** `sudo ss -tulnp` or `sudo netstat -tulnp`

---
### Task: Resolve Hostname to IP Address
* **Tool(s):** `host`, `dig`, `getent hosts`
* **Prompt Example:**
    "Resolve the IP address for the hostname `example.com`. Also, try to find its MX records."
    * **Agent Action Example:**
        ```bash
        echo "--- A Record for example.com ---"
        host example.com
        echo -e "\n--- MX Records for example.com ---"
        host -t mx example.com
        # Alternatively using dig:
        # dig example.com A +short
        # dig example.com MX +short
        ```

---
### Task: Perform a DNS Lookup with Specific Server
* **Tool(s):** `dig`
* **Prompt Example:**
    "Perform a DNS lookup for `internal.corp` using the DNS server `10.0.0.53`. Check for A records."
    * **Agent Action Example:** `dig @10.0.0.53 internal.corp A`

---
### Task: Check Connectivity to a Specific Port on a Remote Host
* **Tool(s):** `nc` (netcat), `nmap` (for quick port check), `curl` (for web ports)
* **Prompt Example (using nc):**
    "Check if TCP port 443 is open and listening on `172.16.50.10`. Use a timeout of 3 seconds."
    * **Agent Action Example:** `nc -zvw3 172.16.50.10 443`
* **Prompt Example (using curl for web):**
    "Attempt to retrieve HTTP headers from `http://targetsite.com:8080`. Report the status code and server header."
    * **Agent Action Example:** `curl -I -m 5 http://targetsite.com:8080`

---
### Task: Trace Route to a Host
* **Tool(s):** `traceroute`, `mtr`
* **Prompt Example:**
    "Trace the network path to `google.com`. Limit to a maximum of 20 hops. Do not resolve IP addresses to hostnames during the trace."
    * **Agent Action Example:** `traceroute -n -m 20 google.com`

---
### Task: Check Public IP Address of Parrot Machine
* **Tool(s):** `curl`, `wget`
* **Prompt Example:**
    "Determine the current public IP address of this Parrot OS machine by querying an external service like `ifconfig.me` or `icanhazip.com`."
    * **Agent Action Example:** `curl -s ifconfig.me/ip` or `curl -s icanhazip.com`
