`# Parrot OS Agent Zero Hacking Prompts

This repository provides an extensive and curated collection of prompts, configurations, and helper tools specifically designed to harness the power of the Agent Zero AI framework for ethical hacking, penetration testing, and security auditing operations within a Parrot OS Security Edition environment.

Overview
Agent Zero is a cutting-edge, personal, and organic agentic framework engineered to learn, adapt, and execute complex tasks based on natural language instructions. Parrot OS, a Debian-based GNU/Linux distribution, is renowned for its comprehensive suite of security, privacy, and development tools, making it a preferred choice for cybersecurity professionals.

This project aims to create a powerful synergy between Agent Zero's AI capabilities and Parrot OS's rich toolset. By providing specialized prompts, we guide Agent Zero to perform a wide array of security assessment tasks more efficiently and effectively. The prompts are structured to reflect real-world penetration testing methodologies, enabling both seasoned professionals and learners to leverage AI in their security workflows.

Key Features & Benefits:

Parrot OS Optimized: Prompts are meticulously crafted and tested for tools, paths, and environment specifics commonly found in Parrot OS Security Edition. This ensures higher reliability and accuracy of agent actions.
Comprehensive Phase-Based Structure: Prompts are logically organized according to standard penetration testing phases (Planning, Reconnaissance, Vulnerability Analysis, Exploitation, Post-Exploitation, Anonymity/Privacy, Reporting). This modular approach allows users to easily select and apply prompts relevant to their current task.
Strong Ethical Hacking Focus: A paramount emphasis is placed on authorized engagements, ethical conduct, and responsible AI usage. Prompts related to potentially impactful actions include built-in cautionary advice and reminders for user confirmation.
Highly Customizable & Extensible: Built upon Agent Zero's flexible prompt architecture, users can easily modify existing prompts or create new ones to suit specific needs, tools, or engagement scenarios.
Educational Value: Provides clear examples of how AI can be instructed to perform complex security tasks, serving as a learning resource for prompt engineering in cybersecurity.
Efficiency Boost: Automates repetitive tasks and assists in complex decision-making, allowing security professionals to focus on higher-level analysis and strategy.
Getting Started
To begin using these Parrot OS-specific prompts with Agent Zero, follow these steps:

Install Agent Zero: Ensure you have a functional Agent Zero instance. Refer to the official Agent Zero installation documentation for detailed instructions.    
Install Parrot OS: A working Parrot OS Security Edition environment is required. This can be a virtual machine (recommended for testing), a container, or a bare-metal installation. Download from the(https://www.parrotsec.org/).    
**Clone this Repository:**bash git clone https://github.com/your-username/parrot-os-agent-zero-prompts.git cd parrot-os-agent-zero-prompts
*(Replace `your-username` with the actual repository location if forked or self-hosted).*
Configure Agent Zero to Use Parrot Prompts:
Option A (Manual Copy): Copy the entire prompts/parrot-hacking/ directory from this repository into your existing Agent Zero prompts/ directory. The path might look something like ~/.agent-zero/prompts/ or wherever your Agent Zero data is stored. 
Bash

# Example: Adjust paths as per your Agent Zero setup
cp -r./prompts/parrot-hacking /path/to/your/agent-zero/prompts/
  
Option B (Docker Volume Mount): If running Agent Zero via Docker, you can mount this repository's prompts directory (or specifically prompts/parrot-hacking) into the container's expected prompt location. When running Agent Zero, select or specify the parrot-hacking prompt set. For example, if using the Docker image:
Bash

# (Assuming you've mounted your custom prompts directory appropriately)
# Make sure./path_to_your_prompts_dir contains the 'parrot-hacking' subdirectory
docker run -it --rm \
  -v./my_agent_zero_data:/data \
  -v./path_to_this_repo/prompts:/app/prompts \
  -e AGENT_PROMPTS=parrot-hacking \
  frdel/agent-zero-run:latest
Option C (Agent Zero UI): If your Agent Zero version supports UI-based prompt set management, you might be able to create a new prompt set that inherits from default and then merges or loads files from the parrot-hacking directory. Refer to your Agent Zero's documentation for specifics.
Core System Prompt
The cornerstone of this prompt set is the "ParrotSec Agent" persona, defined in:
prompts/parrot-hacking/agent.system.md

This system prompt is crucial as it instructs Agent Zero on its designated role, its expected capabilities (specifically mentioning Parrot OS tools), operational procedures, ethical boundaries, and communication style. It's the foundation upon which all other task-specific prompts build.    

Prompt Categories
The prompts are organized for clarity and ease of use:

/prompts/parrot-hacking/phases/: Contains detailed, task-oriented prompts for each stage of a typical penetration test. These are designed to guide the agent through a logical workflow.
00_planning_scoping.md: Prompts for defining objectives, scope, and rules of engagement.
01_reconnaissance.md: Information gathering, target identification, footprinting.
02_vulnerability_analysis.md: Scanning for and identifying weaknesses.
03_exploitation_cautionary.md: (Highly sensitive) Gaining access, with extreme caution and user confirmation.
04_post_exploitation.md: Actions after gaining access – enumeration, privilege escalation, pivoting.
05_anonymity_privacy.md: Leveraging Parrot OS tools for maintaining operational security.
06_reporting_cleanup.md: Documenting findings and reverting changes.
/prompts/parrot-hacking/instruments/: Provides examples for defining custom, reusable Agent Zero "instruments" – sequences of actions packaged as a single command for the agent.    
/prompts/parrot-hacking/common_tasks/: Includes prompts for frequent, general-purpose tasks that might be needed across various phases, such as file management or basic network checks.
Tools
This repository may also include example scripts or configurations that Agent Zero can be prompted to create, use, or manage.

/tools/python/: Contains example Python scripts that Agent Zero can be instructed to write and execute for specialized tasks.    
web_port_checker.py: A simple script to check common (or specified) web ports on a target.
basic_file_hash_checker.py: A script to calculate and compare hashes of files.
Advanced Usage
For more sophisticated techniques, including designing multi-agent architectures, advanced prompt engineering strategies, and operational best practices for complex engagements, please refer to ADVANCED_GUIDE.md.    

Troubleshooting
Common issues and their solutions are documented in TROUBLESHOOTING.md. This includes problems with prompt interpretation, tool execution, and environment setup.    

Ethical Considerations & Disclaimer
⚠️ Agent Zero, especially when equipped with penetration testing prompts, is a powerful tool that can be misused. Operate with extreme caution and responsibility. ⚠️    

Authorized Engagements Only: Under no circumstances should these prompts or Agent Zero be used for any activity targeting systems or networks for which you do not have explicit, written, and verifiable authorization from the asset owner.
Isolated Lab Environment: Always conduct initial testing, prompt development, and learning in a secure, isolated lab environment (e.g., a dedicated virtual network with target VMs you own). This prevents accidental impact on production systems or unauthorized networks.    
Legal and Regulatory Compliance: You are solely responsible for ensuring that all your actions comply with applicable local, national, and international laws, regulations, and ethical guidelines. Ignorance of the law is not an excuse.
User Responsibility: You, the user, are fully responsible and accountable for all actions performed by Agent Zero under your direction and using these prompts. The creators and contributors of this repository are not liable for any misuse or damage caused.
Understand Tool Impact: Before instructing Agent Zero to use any tool, especially those involved in active scanning or exploitation, ensure you understand the tool's behavior, potential impact, and how to interpret its results.
Data Privacy: Handle any sensitive data discovered during authorized engagements with the utmost care, adhering to data protection regulations and the terms of your engagement.    
This project is intended for educational, research, and professional development purposes within the strict confines of ethical hacking and authorized security assessments. Any use for malicious activities is strictly prohibited and against the spirit of this work.

Contributing
Contributions to enhance and expand this prompt library are highly welcome! If you have new prompts, improvements to existing ones, new tool integrations, or bug fixes, please consider contributing.    

How to Contribute:

Fork the Repository: Create your own fork of this project.
Create a Branch: Make your changes in a dedicated branch (e.g., feature/new-nmap-prompts or fix/recon-prompt-typo).
Test Thoroughly: Ensure your changes are well-tested, especially if they involve new tools or complex command sequences.
Document Your Changes: Update any relevant README files or add comments to your prompts explaining their purpose and usage.
Submit a Pull Request: Open a pull request against the main branch of this repository, clearly describing your changes and their rationale.
We also welcome suggestions and bug reports via GitHub Issues.

