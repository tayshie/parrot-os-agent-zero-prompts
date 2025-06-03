file_management.md
# Agent Zero - Parrot OS Hacking Prompts
## Common Task: File and Directory Management

**Objective:** Perform common file system operations within the Parrot OS environment, primarily within the `/work_dir/` or specified project directories.

**General Instructions for Agent:**
* Always confirm paths, especially when deleting or moving files.
* Use standard Linux commands for these operations (`ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`, `find`, `cat`, `echo`, `tee`, `tar`, `zip`, `unzip`).
* Be mindful of permissions. If an operation fails due to permissions, report it and ask if `sudo` should be attempted (if appropriate and safe for the context).

---
### Task: List Directory Contents
* **Tool(s):** `ls`
* **Prompt Example:**
    "List all files and directories, including hidden ones, with detailed information (permissions, owner, size, modification date) in the directory `/work_dir/reconnaissance/`. Present the output clearly."
    * **Agent Action Example:** `ls -lah /work_dir/reconnaissance/`

---
### Task: Create a Directory
* **Tool(s):** `mkdir`
* **Prompt Example:**
    "Create a new directory structure for a new project: `/work_dir/ProjectX/scans/nmap/`. Ensure all parent directories are created if they don't exist."
    * **Agent Action Example:** `mkdir -p /work_dir/ProjectX/scans/nmap/`

---
### Task: Copy Files or Directories
* **Tool(s):** `cp`
* **Prompt Example:**
    "Copy the file `/work_dir/tools/custom_script.py` to `/work_dir/ProjectX/scripts/`. If a file with the same name exists in the destination, create a backup of the existing file before overwriting."
    * **Agent Action Example (Conceptual - might need a small script or sequence for backup):**
        ```bash
        # Agent might respond:
        # "Okay, I will first check if the destination file exists.
        # If it does, I'll attempt to copy it to /work_dir/ProjectX/scripts/custom_script.py.bak
        # Then I will copy the source file. Is this acceptable?"
        # (User confirms)
        # cp --backup=numbered /work_dir/tools/custom_script.py /work_dir/ProjectX/scripts/custom_script.py
        # (Or a more explicit sequence if --backup is not preferred by agent)
        if [ -f "/work_dir/ProjectX/scripts/custom_script.py" ]; then cp "/work_dir/ProjectX/scripts/custom_script.py" "/work_dir/ProjectX/scripts/custom_script.py.bak_$(date +%s)"; fi && cp "/work_dir/tools/custom_script.py" "/work_dir/ProjectX/scripts/"
        ```

---
### Task: Move or Rename Files or Directories
* **Tool(s):** `mv`
* **Prompt Example:**
    "Rename the file `/work_dir/old_report.txt` to `/work_dir/final_report_v2.txt`."
    * **Agent Action Example:** `mv /work_dir/old_report.txt /work_dir/final_report_v2.txt`

---
### Task: Delete Files or Directories
* **Tool(s):** `rm`
* **Prompt Example (with caution):**
    "Delete the directory `/work_dir/temp_files_to_delete/` and all its contents. **Confirm this action is irreversible and the path is correct before proceeding.**"
    * **Agent Action Example:**
        "User, please confirm you want to delete the directory `/work_dir/temp_files_to_delete/` and all its contents. This action cannot be undone. Type 'CONFIRM DELETE /work_dir/temp_files_to_delete/' to proceed."
        *(User confirms)*
        `rm -rf /work_dir/temp_files_to_delete/`

---
### Task: Find Files
* **Tool(s):** `find`
* **Prompt Example:**
    "Find all files ending with `.xml` within `/work_dir/ProjectX/scans/` that were modified in the last 2 days and are larger than 1MB. List their full paths and sizes."
    * **Agent Action Example:** `find /work_dir/ProjectX/scans/ -type f -name "*.xml" -mtime -2 -size +1M -print0 | xargs -0 du -h` (or `find ... -exec ls -lh {} \;`)

---
### Task: View File Content
* **Tool(s):** `cat`, `less`, `head`, `tail`
* **Prompt Example:**
    "Display the first 20 lines and the last 20 lines of the log file `/work_dir/long_scan.log`."
    * **Agent Action Example:**
        ```bash
        echo "--- First 20 lines of /work_dir/long_scan.log ---"
        head -n 20 /work_dir/long_scan.log
        echo -e "\n--- Last 20 lines of /work_dir/long_scan.log ---"
        tail -n 20 /work_dir/long_scan.log
        ```

---
### Task: Archive or Compress Files
* **Tool(s):** `tar`, `zip`
* **Prompt Example:**
    "Create a compressed tarball (gzipped) named `project_archive.tar.gz` in `/work_dir/` containing all files and directories from `/work_dir/ProjectX/final_deliverables/`."
    * **Agent Action Example:** `tar -czvf /work_dir/project_archive.tar.gz -C /work_dir/ProjectX/ final_deliverables/`

---
### Task: Extract Archives
* **Tool(s):** `tar`, `unzip`
* **Prompt Example:**
    "Extract the contents of the archive `/work_dir/downloaded_tools.zip` into a new directory named `/work_dir/tools_extracted/`."
    * **Agent Action Example:** `mkdir -p /work_dir/tools_extracted && unzip /work_dir/downloaded_tools.zip -d /work_dir/tools_extracted/`
