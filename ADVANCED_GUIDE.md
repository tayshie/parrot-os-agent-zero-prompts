ADVANCED_GUIDE.md
# Advanced Guide for Agent Zero on Parrot OS

This guide delves into advanced techniques, multi-agent architectures, sophisticated prompt engineering, and operational best practices for leveraging Agent Zero in complex penetration testing scenarios on Parrot OS. It builds upon the foundational prompts and assumes a good understanding of both Agent Zero and Parrot OS.

## 1. Employing Multi-Agent Architectures

Agent Zero's capability to manage and delegate tasks to subordinate agents is invaluable for complex penetration tests. This allows for specialization and parallel processing of tasks.

**Conceptual Multi-Agent Structure for a Pentest:**

* **Lead Penetration Tester Agent (Human-Supervised or Fully Autonomous):**
    * **Role:** Overall strategic command, coordination, final analysis, and reporting.
    * **System Prompt:** A high-level prompt focusing on project management, delegation, and synthesis of findings.
    * **Interaction:** May receive high-level objectives from a human operator and then break them down for subordinate agents.
* **Subordinate Specialist Agents:**
    * **ReconAgent (ParrotOS-Focused):**
        * **Example System Prompt:** For this agent, a user would create a custom system prompt. It should emphasize tools like `Nmap`, `theHarvester`, `Maltego` casefile generation, and `OSINT-Framework` usage.
        * **Tasks:** Deep network reconnaissance, OSINT, target profiling, identifying attack surfaces.
    * **VulnScanAgent (ParrotOS-Focused):**
        * **Example System Prompt:** A custom prompt for this agent should focus on tools like `Nessus` (if API accessible), `OpenVAS` (via GVM-tools on Parrot), `Nikto`, `Searchsploit`, and custom vulnerability scripting.
        * **Tasks:** Automated and manual vulnerability scanning, exploit research, false positive reduction.
    * **ExploitAgent (ParrotOS-Focused, Highly Restricted):**
        * **Example System Prompt:** This custom prompt requires EXTREME emphasis on safety and user confirmation for *every* step. It would manage interactions with Metasploit (`msfconsole`) and specific exploit scripts.
        * **Tasks:** Controlled exploitation of confirmed vulnerabilities, payload delivery, C2 setup (e.g., using `msfvenom` payloads and listeners).
    * **PostExAgent (ParrotOS-Focused):**
        * **Example System Prompt:** A custom prompt here would focus on Parrot tools for lateral movement, privilege escalation scripts like `LinPEAS`/`WinPEAS`, data exfiltration techniques, and persistence mechanisms.
        * **Tasks:** Internal enumeration, privilege escalation, lateral movement, data exfiltration, maintaining access.
    * **ReportingAgent:**
        * **System Prompt:** A prompt focused on data aggregation, formatting, and report generation (e.g., converting structured data from other agents into Markdown or assisting with report sections).
        * **Tasks:** Compiling findings from other agents, generating draft report sections, tracking evidence.

**Delegation Prompt Example (Lead Agent to ReconAgent):**

"Instantiate a subordinate agent named 'ReconSpecialistAlpha'.
Assign it a custom system prompt you have created for reconnaissance, such as the example 'ReconAgent' prompt described above.
The primary objective for ReconSpecialistAlpha is to conduct thorough external reconnaissance on the organization 'ExampleCorp' with the domain 'examplecorpltd.com'.
Specific tasks include:

Utilize theHarvester with sources 'google,bing,linkedin,crtsh,dnsdumpster' to gather emails, subdomains, and hostnames related to 'examplecorpltd.com'. Limit results to 500 per source.

Perform DNS enumeration using dnsenum on 'examplecorpltd.com', including reverse DNS lookups on discovered netblocks if any.

For any discovered web-facing IP addresses, perform initial Nmap scans: nmap -sV -sC -F --open [target_ip].

Compile all raw outputs into /work_dir/recon_examplecorp/raw/ with clear, timestamped filenames.

Provide a summarized report in Markdown format to /work_dir/recon_examplecorp/summary_recon.md detailing:

Key personnel and email addresses found.

A list of subdomains and their resolved IPs.

A list of external IP addresses with open common ports and identified services.

Any notable observations or potential areas of interest for further investigation.
Confirm when you have successfully initialized ReconSpecialistAlpha and delegated these tasks. Provide updates on its progress periodically."


**Inter-Agent Communication:** Plan how agents will share information. This could be through shared files in `/work_dir/`, a simple messaging protocol defined in prompts, or more advanced mechanisms if Agent Zero supports them.

## 2. Iterative Prompt Engineering for Parrot OS

Optimizing Agent Zero's performance with Parrot OS tools requires a meticulous and iterative approach to prompt engineering:

1.  **Start with Granular Commands:** Test basic, individual commands for Parrot OS tools (e.g., `nmap -sn 192.168.1.1/24`, `nikto -h http://target`). Ensure the agent can execute these correctly and parse their output.
2.  **Tool Path Specificity:** While Parrot OS has standard paths, sometimes tools might be in `/usr/local/bin/` or custom locations. If the agent struggles to find a tool, explicitly provide the full path in the prompt.
3.  **Safe Lab Testing (Crucial):** ALWAYS conduct prompt development and testing in an isolated, virtualized lab environment that mimics your target environment as closely as possible. This prevents accidental scans or actions on unauthorized systems.
4.  **Detailed Observation & Monitoring:** Utilize Agent Zero's interactive terminal or logging features to meticulously observe how it interprets prompts, which commands it formulates, and the raw output it receives. This is key to debugging.
5.  **Analyze Failures and Unexpected Behavior:**
    * **Misinterpretation:** Is the prompt ambiguous? Does it use jargon the agent might not understand in context?
    * **Tool Output Variations:** Does the tool's output change based on target responses in a way the agent isn't prepared for?
    * **Permissions:** Does the command require `sudo`? Is the agent configured to handle this, or does it need to request user intervention? Parrot's `sudo` behavior might differ slightly from other distros.
    * **Environment Differences:** Are there missing dependencies or configurations in the agent's environment compared to a manual Parrot OS terminal?
6.  **Refine, Parameterize, and Re-test:**
    * Modify prompts to be more explicit, break down complex commands, or guide output parsing.
    * Use placeholders like `[target_ip]`, `[output_file]` in your prompts and instruct the agent to substitute them.
    * Test edge cases and different scenarios.
7.  **Leverage Parrot OS Specifics:** If a Parrot OS tool has unique features or output formats (e.g., Anonsurf integration, custom scripts in `/usr/share/parrot-tools/`), craft prompts that leverage these.
8.  **Feedback Loops:** Agent Zero is designed to learn. Provide corrective feedback when it makes mistakes. "No, the correct nmap option for OS detection is `-O`, not `-os_detect`."

Remember Agent Zero's motto: "Communication is Key." Clear, unambiguous, and context-aware prompts are paramount for success, especially when dealing with the diverse and powerful toolset of Parrot OS.

## 3. Critical Security and Ethical Considerations (Reiteration and Expansion)

The power of AI combined with Parrot OS's offensive security tools necessitates an unwavering commitment to ethical conduct and security best practices.

* **DANGER - Amplified Risk:** Agent Zero can execute commands much faster and more persistently than a human. A poorly formulated prompt or a misunderstanding by the agent could lead to widespread, unintended consequences.
* **ISOLATION - Defense in Depth:**
    * **Primary Environment:** Run Agent Zero itself within a container (Docker) or a dedicated VM.
    * **Target Environment:** Ensure your penetration testing lab is on a completely isolated network segment, with no routes to production or sensitive networks.
    * **Parrot OS VM:** Consider running Parrot OS as a VM, which Agent Zero then interacts with, adding another layer of separation.
* **AUTHORIZATION - Zero Trust Approach:**
    * Verify authorization documents.
    * Clearly define and confirm the scope with the client *before* any active engagement.
    * Embed scope limitations directly into high-level system prompts for specialist agents.
* **LEGALITY - Jurisdictional Awareness:** Be aware that laws regarding network scanning, vulnerability research, and data access vary significantly by jurisdiction. Ensure your engagement and actions are legal where the target systems reside and where you are operating from.
* **RESPONSIBILITY - The "Human in the Loop":** While aiming for automation, maintain a "human in theloop" for critical decisions, especially concerning exploitation or actions that modify target systems. You are the operator and bear ultimate responsibility.
* **DATA PRIVACY & MINIMIZATION:**
    * During post-exploitation, instruct the agent to only collect data strictly within the scope of the engagement.
    * Avoid accessing or exfiltrating PII unless explicitly authorized and necessary for the test objectives.
    * Implement secure data handling and deletion protocols for any sensitive information gathered.
* **TOOL USAGE AGREEMENTS:** Some commercial tools integrated into Parrot OS or used alongside it may have specific license terms. Ensure compliance.

## 4. Custom Instrument Development for Parrot OS Workflows

Agent Zero's "instruments" (reusable, parameterized sequences of actions) are powerful for encapsulating common Parrot OS workflows.

**Example: Advanced Web Application Recon Instrument**

"Define a new instrument named 'ParrotWebAppRecon'.
This instrument accepts two arguments: 'target_url' (e.g., https://example.com) and 'output_basename' (e.g., example_com_recon).

The instrument must perform the following sequence of actions using Parrot OS tools, saving all outputs to /work_dir/web_recon/[output_basename]/:

Initial Headers & Tech Stack (whatweb):

Command: whatweb -v [target_url] > /work_dir/web_recon/[output_basename]/whatweb_verbose.txt

Purpose: Identify web technologies, server versions, cookies, and interesting headers.

SSL/TLS Scan (testssl.sh): (Parrot often includes testssl.sh or it's easily added)

Command: testssl.sh --htmlfile /work_dir/web_recon/[output_basename]/testssl_report.html [target_url_hostname_only] (Extract hostname from target_url)

Purpose: Comprehensive SSL/TLS security assessment.

Directory & File Brute-forcing (gobuster):

Command: gobuster dir -u [target_url] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,js,bak,config -o /work_dir/web_recon/[output_basename]/gobuster_medium.txt -t 50

Purpose: Discover hidden directories and files.

Screenshot (if gowitness or similar is available):

Command (conceptual): gowitness single [target_url] -P /work_dir/web_recon/[output_basename]/screenshots/

Purpose: Visual confirmation of web pages.

Summary Report Generation:

Action: Parse key findings from whatweb_verbose.txt (e.g., Server, X-Powered-By, interesting cookies) and gobuster_medium.txt (any 200/301/302 status codes).

Output: Create /work_dir/web_recon/[output_basename]/summary.md with these key findings.

Store the definition of this 'ParrotWebAppRecon' instrument.
Report back when the instrument is defined and ready for use, listing its arguments."

(Refer to `prompts/parrot-hacking/instruments/quick_host_recon_instrument_def.md` and `web_app_header_check_instrument_def.md` for other examples.)

## 5. Output Management and Reporting for Parrot OS Engagements

Effective output management is crucial for any penetration test. Parrot OS provides many tools, and their outputs need to be handled systematically.

* **Standardized Directory Structure:**
    * Main engagement directory: `/work_dir/[client_project_name]/`
    * Phase-based subdirectories: `.../01_recon/`, `.../02_vuln_analysis/`, etc.
    * Tool-specific subdirectories: `.../01_recon/nmap/`, `.../01_recon/theharvester/`
* **Clear Naming Conventions:**
    * `[tool]_[target_identifier]_[scan_type]_[timestamp].[format]`
    * Example: `nmap_192.168.1.10_fulltcp_202406031030.xml`
* **Multiple Output Formats:** Instruct Agent Zero to save tool outputs in various formats when available:
    * **Text (`.txt`):** Human-readable.
    * **XML (`.xml`):** For parsing by other tools (e.g., Nmap XML into Metasploit).
    * **Grepable (`.gnmap`):** For easy searching with `grep`.
    * **JSON (`.json`):** Modern, structured format for many tools.
    * **HTML (`.html`):** For reports from tools like `testssl.sh` or `nikto`.
* **Automated Summaries:** Prompt the agent to parse raw outputs and generate concise summaries or lists of key findings (e.g., "List all open TCP ports from the Nmap XML output," "Extract all email addresses from theHarvester text output").
* **Evidence Logging:** Instruct the agent to maintain a log of commands executed and their immediate results, timestamped. This can be part of its core system prompt or a specific instruction for sensitive operations.
* **Integration with Parrot Reporting Tools:** If Parrot OS has specific reporting tools or templates (e.g., Dradis, Serpico, or even just Pandoc for Markdown to PDF conversion), prompt Agent Zero to format its findings or use these tools.

**Example Prompt for Structured Output and Parsing:**

"Execute nmap -sV -sC -O -p- --reason --open -T4 [target_IP] -oA /work_dir/[target_IP]_nmap_comprehensive.
This will save output in Normal, XML, and Grepable formats using the basename provided.
After the scan completes:

Parse the XML output file (/work_dir/[target_IP]_nmap_comprehensive.xml).

Extract and list the following details for each open port:

Port number

Protocol (TCP/UDP)

Service name

Service version

Operating System guess (if available)

Present this extracted information in a Markdown table.

Additionally, count the total number of open TCP ports and report this count."


By implementing these advanced strategies, you can significantly elevate the sophistication, efficiency, and control of your Agent Zero-assisted penetration testing activities on Parrot OS. Continuous learning and adaptation of prompts based on experience are key to mastering this powerful combination.