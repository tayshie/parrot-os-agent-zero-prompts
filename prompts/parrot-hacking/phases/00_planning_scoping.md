00_planning_scoping.md
# Agent Zero - Parrot OS Hacking Prompts
## Phase: 00 - Planning, Scoping, and Authorization

**Objective:** Define the objectives, scope, rules of engagement, and confirm authorization for the penetration test. This phase is crucial for a successful and ethical engagement. Agent Zero's role here is primarily to document and remind, not to make decisions.

**General Instructions for Agent:**
* Your role in this phase is to assist the human operator in documenting critical information.
* Prompt the user for necessary details if they are missing.
* Store all planning and scoping information securely in `/work_dir/planning_and_scoping/`.
* Emphasize the importance of written authorization.

---
### Task: Document Engagement Objectives
* **Prompt Example:**
    "Let's document the primary objectives for this penetration test. Please provide a clear statement of what we aim to achieve (e.g., 'Identify critical vulnerabilities in the external web application suite,' 'Assess the security of the internal wireless network,' 'Attempt to gain domain administrator privileges from an assumed breach scenario').
    I will save this as `/work_dir/planning_and_scoping/objectives.md`."
    *(Agent waits for user input and saves it)*

---
### Task: Define Scope of Testing
* **Prompt Example:**
    "Define the scope for this engagement. Please list all IP addresses, ranges, domains, applications, or systems that are **IN SCOPE**.
    Also, explicitly list any IP addresses, ranges, domains, applications, or systems that are **OUT OF SCOPE**.
    I will save this as `/work_dir/planning_and_scoping/scope.md`."
    *(Agent waits for user input and saves it, perhaps prompting for format like "In-scope IPs: [list]", "Out-of-scope domains: [list]")*

---
### Task: Establish Rules of Engagement (RoE)
* **Prompt Example:**
    "Let's outline the Rules of Engagement. Consider the following points and provide the agreed-upon rules:
    1.  **Timing of Tests:** Are there specific windows for testing (e.g., only after business hours)?
    2.  **Allowed Techniques:** Are there any forbidden techniques (e.g., no DoS testing, no social engineering, specific exploits to avoid)?
    3.  **Critical Systems:** Are there any systems that, if impacted, would cause major disruption? How should these be handled?
    4.  **Data Handling:** How should sensitive data encountered during the test be handled, stored, and reported?
    5.  **Communication Channels:** Primary points of contact for the client and for our team? Emergency contact procedures?
    6.  **Evidence Collection:** Specific requirements for screenshots, logs, or command outputs?
    I will save this as `/work_dir/planning_and_scoping/rules_of_engagement.md`."
    *(Agent waits for user input and saves it)*

---
### Task: Confirm Written Authorization
* **Prompt Example:**
    "**CRITICAL REMINDER:** Before any active testing begins, ensure we have received and verified **written authorization** from the asset owner for this engagement, clearly stating the approved scope and objectives.
    Has written authorization been obtained and verified? (Yes/No)
    If yes, please provide the filename or reference for the authorization document (e.g., `client_authorization_signed.pdf`). I will note this in `/work_dir/planning_and_scoping/authorization_confirmation.md`."
    *(Agent waits for user input. If 'No', it should strongly advise against proceeding with active testing.)*
    If user says 'Yes' and provides a reference:
    "Noted: Written authorization confirmed. Reference: `[UserProvidedReference]`. Saved to `/work_dir/planning_and_scoping/authorization_confirmation.md`."

---
### Task: Identify Tools and Resources (Parrot OS)
* **Prompt Example:**
    "Based on the objectives and scope, let's list the key Parrot OS tools we anticipate using for each phase. This helps in preparation.
    For example:
    * Reconnaissance: `nmap`, `theHarvester`, `dnsenum`, `whatweb`
    * Vulnerability Analysis: `nikto`, `searchsploit`, `nmap NSE scripts`
    * Exploitation: `msfconsole`
    * Post-Exploitation: `LinPEAS`, standard Linux enumeration commands
    Please list any other specific tools or wordlists from Parrot OS we should prepare. I'll save this as `/work_dir/planning_and_scoping/tool_checklist.md`."
    *(Agent waits for user input and saves it)*

---
### Task: Create Project Directory Structure
* **Prompt Example:**
    "I will now create a standardized directory structure for this engagement within `/work_dir/` based on the project name you provide. What is the project name or client identifier for this engagement (e.g., 'ClientXYZ_Q3_Pentest')?"
    *(User provides project name, e.g., 'AcmeCorp_WebApp_Test')*
    "Okay, creating the following structure:
    `/work_dir/AcmeCorp_WebApp_Test/`
    `/work_dir/AcmeCorp_WebApp_Test/00_planning_scoping/`
    `/work_dir/AcmeCorp_WebApp_Test/01_reconnaissance/`
    `/work_dir/AcmeCorp_WebApp_Test/02_vulnerability_analysis/`
    `/work_dir/AcmeCorp_WebApp_Test/03_exploitation/`
    `/work_dir/AcmeCorp_WebApp_Test/04_post_exploitation/`
    `/work_dir/AcmeCorp_WebApp_Test/05_reporting/`
    `/work_dir/AcmeCorp_WebApp_Test/loot/`
    `/work_dir/AcmeCorp_WebApp_Test/evidence/`
    `/work_dir/AcmeCorp_WebApp_Test/custom_scripts/`
    Is this structure acceptable? I will then move the planning documents we've created into `/work_dir/AcmeCorp_WebApp_Test/00_planning_scoping/`."
    *(Agent executes mkdir commands and mv commands upon confirmation)*
