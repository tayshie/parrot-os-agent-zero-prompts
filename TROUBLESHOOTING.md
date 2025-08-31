# Troubleshooting Agent Zero with Parrot OS Prompts

This document provides solutions and guidance for common issues encountered when using Agent Zero with the Parrot OS Hacking Prompts.

## 1. Agent Fails to Find or Execute Tools

* **Symptom:** Agent reports "command not found," "tool not installed," or fails to execute a Parrot OS specific tool.
* **Possible Causes & Solutions:**
    * **Incorrect Path:** While Parrot OS has standard paths, some tools might be in non-standard locations or the agent's environment PATH might be incomplete.
        * **Solution:** In your prompt, specify the full path to the tool (e.g., `/usr/sbin/nmap` instead of just `nmap`). You can find tool paths in Parrot OS using `which <toolname>` or `whereis <toolname>`.
    * **Permissions:** The tool might require `sudo` privileges.
        * **Solution:** Ensure your `agent.system.md` or specific task prompt allows the agent to request `sudo` or handles it appropriately. For Parrot OS, you might have passwordless `sudo` configured for certain commands, or the agent needs to be able to ask for the password.
    * **Tool Not Installed (Unlikely in Full Parrot OS):** In minimal Parrot OS installs or custom environments, a tool might genuinely be missing.
        * **Solution:** Instruct the agent to install the tool using `sudo apt update && sudo apt install -y <toolname>`, but only if you are certain this is safe and intended.
    * **Environment Variables:** Some tools rely on specific environment variables.
        * **Solution:** Ensure these are set in the agent's execution environment or instruct the agent to set them before running the tool (e.g., `export VARNAME=value && tool_command`).

## 2. Prompts Are Misinterpreted or Lead to Incorrect Actions

* **Symptom:** Agent Zero performs an action different from what was intended, uses incorrect tool options, or gets stuck in a loop.
* **Possible Causes & Solutions:**
    * **Ambiguity:** The prompt might be unclear or use language that can be interpreted in multiple ways.
        * **Solution:** Be more specific. Break down complex instructions into smaller, simpler steps. Define jargon or provide examples.
    * **Lack of Context:** The agent might not understand the broader context of the penetration testing phase or objective.
        * **Solution:** Ensure the phase-specific prompts provide enough background. The `agent.system.md` should establish the overall role well.
    * **Overly Complex Commands:** Trying to make the agent construct a very long and complex single command can lead to errors.
        * **Solution:** Break it into multiple simpler commands. Use intermediate files if necessary.
    * **Tool Output Variations:** The agent might be expecting a certain output format from a tool, but the target system causes the tool to behave differently.
        * **Solution:** Make prompts more robust to variations in output. Instruct the agent on how to handle common error messages or unexpected results from tools.

## 3. Issues with Anonymity Tools (Anonsurf, torsocks)

* **Symptom:** Anonsurf fails to start, `torsocks` doesn't route traffic correctly, or IP address doesn't change as expected.
* **Possible Causes & Solutions:**
    * **Anonsurf Service Issues:** The Anonsurf service or Tor might not be running correctly in the Parrot OS environment.
        * **Solution:** Manually check `sudo systemctl status anonsurf` or `tor` service status in Parrot OS. Instruct agent to restart services if necessary (with caution).
    * **DNS Leaks:** Even with Tor, DNS requests might leak.
        * **Solution:** Parrot's Anonsurf aims to prevent this. If using `torsocks`, ensure DNS resolution is also happening over Tor (often default with `torsocks`). Explicitly prompt the agent to verify DNS resolution if critical.
    * **Conflicting Network Configurations:** Custom network setups or VPNs might interfere.
        * **Solution:** Simplify the network configuration for testing. Ensure only one primary anonymization method is active.

## 4. Output Management Problems

* **Symptom:** Files are not saved where expected, filenames are incorrect, or data is overwritten.
* **Possible Causes & Solutions:**
    * **Incorrect Paths in Prompts:** Typos or incorrect directory structures in the prompts.
        * **Solution:** Double-check all file paths specified in prompts. Use absolute paths for `/work_dir/` if relative paths are causing confusion.
    * **Permissions to Write:** The agent might not have permission to write to the specified directory.
        * **Solution:** Ensure `/work_dir/` (or its equivalent in the agent's environment) is writable by the user the agent runs as.
    * **Timestamp/Uniqueness:** If not using unique filenames (e.g., with timestamps), subsequent runs might overwrite previous results.
        * **Solution:** Include instructions in prompts to use timestamps or other unique identifiers in filenames. The `ADVANCED_GUIDE.md` provides examples.

## 5. Agent Seems "Stuck" or Unresponsive

* **Symptom:** Agent Zero stops processing, doesn't respond to new prompts, or seems to be in a loop.
* **Possible Causes & Solutions:**
    * **Waiting for Long-Running Command:** A tool like `nmap -p-` can take a very long time. The agent might be waiting for it to finish.
        * **Solution:** Instruct the agent to run long commands in the background if appropriate, or to provide periodic updates. Set reasonable timeouts for tools if possible.
    * **Resource Exhaustion:** The agent or the tools it's running might be consuming too much CPU or memory.
        * **Solution:** Monitor system resources on the machine running Agent Zero and/or the Parrot OS environment. Optimize prompts to use less resource-intensive tool options where feasible.
    * **Internal Agent Error:** There might be an issue within Agent Zero itself.
        * **Solution:** Check Agent Zero's logs for any internal error messages. Restart Agent Zero. If persistent, report the issue to the Agent Zero developers.

## General Tips for Better Results:

* **Start Simple:** Test individual tool commands before combining them into complex sequences.
* **Be Explicit:** Don't assume the agent knows implicit steps. Spell them out.
* **Iterate:** Prompt engineering is an iterative process. Test, observe, refine, and re-test.
* **Use the `/work_dir/`:** Consistently use this directory for outputs so the agent (and you) know where to find results.
* **Consult Agent Zero Documentation:** Refer to the official Agent Zero documentation for general troubleshooting and best practices related to the framework itself.

If you encounter an issue not listed here, consider opening an issue on this repository's GitHub page with detailed information about the prompt used, the observed behavior, and any error messages.
