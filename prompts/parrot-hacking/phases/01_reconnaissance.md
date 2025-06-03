01_reconnaissance.md
# Agent Zero - Parrot OS Hacking Prompts
## Phase: 01 - Reconnaissance & Enumeration

**Objective:** Systematically gather comprehensive information about the target system(s), network(s), and associated entities without active intrusion where possible. Leverage Parrot OS's extensive suite of tools for OSINT, network discovery, service identification, and initial vulnerability mapping.

**General Instructions for Agent:**
* All outputs, raw data, and summaries should be saved to `/work_dir/[project_name]/01_reconnaissance/[tool_name]/` in clearly named files (e.g., `nmap_initial_sweep_[target_range_for_filename].txt`). The `[project_name]` should be established during planning.
* Summarize key findings concisely after each major task or tool execution. Highlight any particularly interesting or unexpected discoveries.
* If unsure about a command's impact, or if a command might be too "loud" for the current ROE (Rules of Engagement), ask for clarification or user confirmation.
* Remember to check for `sudo` requirements if permission issues arise for tools like `nmap` (for certain scan types) or `arp-scan`. Confirm with the user first if not explicitly stated in the system prompt for benign discovery commands or if ROE restricts `sudo` usage.
* Correlate findings from different tools to build a more complete picture of the target.

---
### Task: Passive Reconnaissance - OSINT (Open-Source Intelligence)
* **Tool(s):** `theHarvester`, `recon-ng` (if agent is proficient), manual browsing (conceptual for agent), `metagoofil`
* **Prompt Example (theHarvester):**
    "Utilize `theHarvester` to gather open-source intelligence for the domain `[target_domain.com]`.
    Employ a comprehensive set of data sources available in Parrot's `theHarvester` (e.g., `google`, `bing`, `duckduckgo`, `linkedin`, `crtsh`, `dnsdumpster`, `virustotal`, `shodan-org`).
    Limit results to a reasonable number per source (e.g., 300).
    Save the complete output in both XML and HTML formats to `/work_dir/[project_name]/01_reconnaissance/theHarvester/theHarvester_[target_domain_for_filename]`.
    Report a summary including: total unique emails, subdomains, virtual hosts, IPs, and any interesting employee names or roles discovered."
* **Prompt Example (metagoofil for metadata):**
    "Use `metagoofil` to search for public documents related to `[target_domain.com]` using Google (filetype:pdf, doc, xls, ppt, etc.).
    Download a small number (e.g., limit to 20) of these documents to `/work_dir/[project_name]/01_reconnaissance/metagoofil/docs/`.
    Extract metadata from these downloaded documents.
    Save the metadata report to `/work_dir/[project_name]/01_reconnaissance/metagoofil/metadata_report_[target_domain_for_filename].txt`.
    Summarize any usernames, software versions, or paths found in the metadata."

---
### Task: Active Reconnaissance - Network Sweeping & Host Discovery
* **Tool(s):** `nmap`, `masscan`, `arp-scan` (for local network discovery)
* **Prompt Example (Nmap Ping Sweep):**
    "Perform an Nmap ping scan (`-sn`) on the subnet `[target_subnet_cidr]` (e.g., 192.168.1.0/24 or a list of external IPs) to identify live hosts. Use ARP discovery (`-PR`) if on the local segment, and consider ICMP echo, TCP SYN to port 443, TCP ACK to port 80, and ICMP timestamp requests (`-PE -PS443 -PA80 -PP`) for more robust discovery.
    Save the list of live hosts (IP and MAC if available) to `/work_dir/[project_name]/01_reconnaissance/nmap/live_hosts_[target_subnet_for_filename].txt`.
    Report the number of live hosts found and list their IP addresses."
* **Prompt Example (arp-scan for local LAN):**
    "If we are on the local network segment `[local_subnet_cidr, e.g., 10.0.0.0/24]`, use `sudo arp-scan --localnet` (or specify interface with `-I [interface_name]`) to discover all live hosts on this LAN segment.
    Save the output to `/work_dir/[project_name]/01_reconnaissance/arp-scan/local_lan_hosts.txt`.
    Report the discovered IP and MAC address pairs."

---
### Task: Port Scanning and Service Identification
* **Tool(s):** `nmap`, `masscan` (for very large ranges, followed by Nmap for service detection)
* **Prompt Example (Nmap Basic Port Scan on Live Hosts):**
    "For each live host identified in `/work_dir/[project_name]/01_reconnaissance/nmap/live_hosts_[target_subnet_for_filename].txt` (or provide a list: `[ip1,ip2,...]`), perform an Nmap scan for the top 1000 TCP ports (`--top-ports 1000`) and top 100 UDP ports (`-sU --top-ports 100`). Include service version detection (`-sV`), default scripts (`-sC`), and OS detection (`-O`). Use `-T4` timing.
    Save individual Nmap outputs in XML, Nmap, and Grepable formats to `/work_dir/[project_name]/01_reconnaissance/nmap/detailed_scan_[host_ip]`.
    Compile a summary table (Markdown) of all unique open ports found across all scanned hosts, listing IP, Port, Protocol, Service, and Version."
* **Prompt Example (Nmap Full TCP Port Scan on High-Value Target):**
    "Conduct an exhaustive Nmap TCP scan on the high-value target `[target_ip]`. Scan all 65535 TCP ports (`-p-`). Include service version detection (`-sV --version-intensity 7`), OS detection (`-O --osscan-guess`), default scripts (`-sC`), and traceroute (`--traceroute`). Use `-T3` timing to be less aggressive. Add `--reason`.
    Save the full output in all formats (`-oA`) to `/work_dir/[project_name]/01_reconnaissance/nmap/full_tcp_scan_[target_ip]`.
    Report a detailed summary of open ports, services, versions, detected OS, and any interesting script outputs."

---
### Task: DNS Enumeration & Zone Transfers
* **Tool(s):** `dnsenum`, `dig`, `host`, `fierce` (if available in Parrot)
* **Prompt Example (dnsenum):**
    "Perform comprehensive DNS enumeration on `[target_domain.com]` using `dnsenum`.
    Ensure you attempt to get A, NS, MX records, perform a zone transfer attempt (`-f /usr/share/dnsenum/dns.txt` for brute-forcing subdomains if zone transfer fails), use Google scraping (`-g`), and reverse lookups on discovered netblocks.
    Save the full output to `/work_dir/[project_name]/01_reconnaissance/dnsenum/dnsenum_[target_domain_for_filename].xml` (if XML output is supported, else .txt).
    Summarize key findings: Name servers, mail servers, any successful zone transfers, a list of discovered subdomains and their IPs, and any identified netblocks."
* **Prompt Example (dig for specific records):**
    "Using `dig`, query for `ANY`, `TXT`, `SRV`, and `SPF` records for `[target_domain.com]`. Also check for potential subdomain takeover vulnerabilities by looking for CNAMEs pointing to services like S3, Heroku, GitHub Pages, etc., that might be unclaimed (e.g., `dig CNAME _something_.example.com`).
    Save outputs to `/work_dir/[project_name]/01_reconnaissance/dig/dig_extra_records_[target_domain_for_filename].txt`."

---
### Task: Web Server Discovery & Enumeration
* **Tool(s):** `nmap` (HTTP/HTTPS scripts), `whatweb`, `httpx` (if available), `dirb`, `gobuster`, `nikto` (for initial light scan)
* **Prompt Example (whatweb for tech identification):**
    "For each web server identified (e.g., `http://[target_ip_or_domain]:[port]`, `https://[target_ip_or_domain]:[port]`), use `whatweb -v -a 3` to identify web technologies, server versions, CMS, JavaScript libraries, and other interesting details.
    Save individual outputs to `/work_dir/[project_name]/01_reconnaissance/whatweb/whatweb_[target_for_filename].txt`.
    Compile a list of unique technologies identified across all targets."
* **Prompt Example (gobuster for directory/file brute-forcing):**
    "Use `gobuster dir` to scan the web application at `http://[target_ip_or_domain]/` for common directories and files.
    Employ the wordlist `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`.
    Scan for extensions: `php,html,htm,js,txt,bak,config,env,zip,tar.gz`.
    Use a moderate number of threads (e.g., `-t 30`). Follow redirects. Exclude status codes 404, 403 (if too noisy, adjust).
    Save the output to `/work_dir/[project_name]/01_reconnaissance/gobuster/gobuster_dir_[target_for_filename].txt`.
    Report any discovered paths that return 200 OK, 301/302 Redirect, or other interesting status codes (e.g., 500 indicating an error that might leak info)."

---
### Task: SMB/NFS Enumeration (If Applicable)
* **Tool(s):** `nmap` (smb-enum-* scripts, rpcinfo), `enum4linux-ng` (Parrot often has this or similar), `showmount -e`
* **Prompt Example (Nmap SMB enumeration):**
    "If target `[target_ip]` has SMB ports (139, 445) open, use Nmap with scripts `smb-enum-shares`, `smb-enum-users`, `smb-os-discovery`, `smb-protocols`, `smb-security-mode`, and `smb2-capabilities`.
    Save output to `/work_dir/[project_name]/01_reconnaissance/nmap_smb/nmap_smb_enum_[target_ip].txt`.
    Report discovered shares (and their permissions if possible), user accounts, OS details, SMB protocol versions, and security mode."
* **Prompt Example (NFS enumeration):**
    "If target `[target_ip]` has NFS port (2049 or 111 for rpcbind) open, use `showmount -e [target_ip]` to list exported NFS shares. Also use `nmap -sV -p 111,2049 --script rpcinfo,nfs-ls,nfs-showmount [target_ip]`.
    Save output to `/work_dir/[project_name]/01_reconnaissance/nfs/nfs_enum_[target_ip].txt`.
    Report any accessible NFS shares and their allowed access."

---
### Task: SNMP Enumeration (If Applicable)
* **Tool(s):** `snmpwalk`, `snmp-check`, `nmap` (snmp-* scripts)
* **Prompt Example (snmp-check):**
    "If target `[target_ip]` has SNMP port (161/UDP) open, attempt to enumerate information using `snmp-check [target_ip]` with common community strings like `public`, `private`, `manager`. If a specific community string is known, use it.
    Save the output to `/work_dir/[project_name]/01_reconnaissance/snmp/snmp_check_[target_ip].txt`.
    Report any interesting information found, such as network interfaces, routing tables, software versions, or user accounts."

---
### Task: Screenshot Web Services (Optional, for visual context)
* **Tool(s):** `gwenhywfar` (part of Aquatone, or similar like `gowitness` if installed/instructed)
* **Prompt Example (conceptual, assuming tool availability):**
    "If a web screenshotting tool like `gowitness` or `eyewitness` is available and configured in this Parrot OS environment:
    Take screenshots of all web services (HTTP/HTTPS on common ports like 80, 443, 8080, 8443) discovered on the live hosts listed in `/work_dir/[project_name]/01_reconnaissance/nmap/live_hosts_with_web_ports.txt`.
    Save screenshots to `/work_dir/[project_name]/01_reconnaissance/screenshots/`.
    Report completion and the number of screenshots taken."
    *(Note: This may require Agent Zero to install the tool or for it to be pre-available. Confirm tool path and usage.)*
