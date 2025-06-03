06_reporting_cleanup.md
# Agent Zero - Parrot OS Hacking Prompts
## Phase: 06 - Reporting & Cleanup

**Objective:** Consolidate all findings, evidence, and logs into a comprehensive report. Perform any necessary cleanup actions on target systems (if authorized and possible) and on the attacker machine as per the Rules of Engagement.

**General Instructions for Agent:**
* Your primary role in reporting is to help gather, structure, and format data. The final analysis and narrative are typically human-driven.
* All reporting materials should be saved to `/work_dir/[project_name]/05_reporting/`.
* Cleanup actions are highly sensitive and MUST be explicitly authorized and confirmed for each step.
* Prioritize non-destructive cleanup.

---
### Task: Consolidate Findings and Evidence
* **Prompt Example:**
    "Let's begin compiling the report for `[project_name]`.
    1.  Gather all summary files and key output logs from each phase directory:
        * `/work_dir/[project_name]/01_reconnaissance/...`
        * `/work_dir/[project_name]/02_vulnerability_analysis/...`
        * `/work_dir/[project_name]/03_exploitation/...`
        * `/work_dir/[project_name]/04_post_exploitation/...`
    2.  Create a structured list of all identified vulnerabilities, including:
        * Vulnerability Name/Type
        * Affected Host(s)/URL(s)
        * Severity (e.g., Critical, High, Medium, Low - CVSS if available)
        * Brief Description
        * Evidence (path to log file or screenshot)
        * Recommended Remediation
    3.  Organize screenshots, loot (e.g., exfiltrated flags, config files), and critical log files into an `evidence_package` subdirectory.
    I will save the structured vulnerability list as `/work_dir/[project_name]/05_reporting/vulnerability_summary.md`. You can assist by parsing specific log files for key information as requested."

---
### Task: Draft Report Sections (Agent Assistance)
* **Prompt Example:**
    "Assist in drafting the 'Executive Summary' section of the report. Based on the most critical vulnerabilities found (e.g., [list a few critical ones]), provide a brief, high-level overview of the security posture and potential business impact. Keep it concise (2-3 paragraphs)."
    *(Agent generates text based on prior knowledge of findings)*

* **Prompt Example:**
    "For the vulnerability '[Specific Vulnerability Name, e.g., SQL Injection in login.php]', draft a detailed finding description. Include:
    1.  A technical description of the vulnerability.
    2.  Steps to reproduce (referencing specific tools/commands used from logs).
    3.  The potential impact if exploited.
    4.  Paths to relevant evidence files.
    I will then refine this for the final report."
    *(Agent generates text by pulling from its logs and understanding of the vulnerability)*

---
### Task: Generate Tool Outputs in Report-Friendly Formats
* **Prompt Example:**
    "Many tools like Nmap, Nikto, testssl.sh can output in HTML. If we have XML outputs from Nmap for key scans (e.g., `/work_dir/[project_name]/01_reconnaissance/nmap/detailed_scan_[host_ip].xml`), convert them to an HTML report using `xsltproc` (if available on Parrot OS) or suggest a method.
    For example: `xsltproc /usr/share/nmap/nmap.xsl /path/to/nmap.xml -o /path/to/nmap_report.html`."
    *(Agent checks for xsltproc and nmap.xsl, then provides command or alternative)*

---
### Task: Target System Cleanup (EXTREMELY CAUTIOUS - REQUIRES EXPLICIT AUTHORIZATION)
* **Prompt Example (Removing uploaded files):**
    "The Rules of Engagement for `[project_name]` require us to remove any tools or files uploaded to target systems, if possible and authorized.
    During post-exploitation on `[target_ip_or_hostname]`, we uploaded `linpeas.sh` to `/tmp/linpeas.sh` and created `/tmp/linpeas_output.txt`.
    Are we authorized to remove these specific files?
    If user confirms 'USER_CONFIRMS_REMOVE_TARGET_FILES [target_ip] /tmp/linpeas.sh /tmp/linpeas_output.txt':
    Execute `rm /tmp/linpeas.sh /tmp/linpeas_output.txt` on the target system via our existing shell.
    Log this action to `/work_dir/[project_name]/05_reporting/cleanup_log.txt`."

* **Prompt Example (Reverting minor changes - e.g., a cron job for persistence):**
    "During post-exploitation, we added a cron job for user `[user_on_target]` for persistence: `[cron_job_details]`.
    Are we authorized to remove this specific cron job?
    If user confirms 'USER_CONFIRMS_REMOVE_CRON_JOB [target_ip] [user_on_target]':
    Explain the command to remove it (e.g., `(crontab -u [user_on_target] -l | grep -v '[pattern_from_cron_job_details]' | crontab -u [user_on_target] -)` ) and execute it on the target.
    Log this action."
    **Agent Note: Reverting complex changes or system modifications should generally be handled by the client's IT team based on report recommendations, not directly by the pentester unless explicitly and safely agreed.**

---
### Task: Attacker Machine Cleanup (As per RoE and `05_anonymity_privacy.md`)
* **Prompt Example:**
    "Referencing Phase 05 (`05_anonymity_privacy.md`) and the Rules of Engagement for `[project_name]`, are there any specific cleanup actions required on this Parrot OS attacker machine (e.g., clearing specific logs, securely deleting temporary sensitive files created during the engagement)?
    For example, if we created `/work_dir/[project_name]/temp_credentials.txt`, and RoE allows, confirm shredding: 'USER_CONFIRMS_SHRED_ATTACKER_FILE /work_dir/[project_name]/temp_credentials.txt'.
    Execute confirmed actions and log them to `/work_dir/[project_name]/05_reporting/attacker_cleanup_log.txt`."

---
### Task: Final Report Archival
* **Prompt Example:**
    "All report sections and evidence have been compiled into `/work_dir/[project_name]/05_reporting/Final_Pentest_Report_[project_name].pdf` (assuming human compiled it or agent assisted in Markdown-to-PDF).
    Create a compressed, encrypted archive (e.g., 7zip or GPG tarball) of the entire `/work_dir/[project_name]/` directory, named `[project_name]_pentest_archive_encrypted.[7z|gpg]`.
    Prompt the user for a strong password for encryption.
    Store the archive in `/work_dir/archived_projects/`.
    Example (conceptual for GPG):
    `tar czvf - /work_dir/[project_name]/ | gpg --symmetric --cipher-algo AES256 -o /work_dir/archived_projects/[project_name]_pentest_archive.tar.gz.gpg` (after prompting for passphrase).
    Advise user to securely store the passphrase."
