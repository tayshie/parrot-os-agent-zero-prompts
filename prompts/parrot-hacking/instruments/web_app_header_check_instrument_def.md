web_app_header_check_instrument_def.md`
```markdown
# Agent Zero - Parrot OS Hacking Prompts
## Instrument Definition: WebAppHeaderCheck

**Objective:** Define a reusable Agent Zero instrument to fetch and analyze HTTP/S headers from a given web application URL, focusing on security-relevant headers.

**Instrument Name:** `WebAppHeaderCheck`

**Argument(s):**
* `target_url`: (String) The full URL of the web application to check (e.g., "[https://example.com/login.php](https://example.com/login.php)").
* `output_tag`: (String, Optional) A tag for the output filename.

**Sequence of Actions (using Parrot OS tools):**

1.  **Fetch HTTP/S Headers:**
    * **Tool:** `curl`
    * **Command:** `curl -sSLk -I [target_url]`
        * `-s`: Silent mode.
        * `-S`: Show error.
        * `-L`: Follow redirects.
        * `-k`: Allow insecure server connections (useful for self-signed certs in labs, but note this in output).
        * `-I`: Fetch headers only (HEAD request).
    * **Purpose:** Retrieve all HTTP/S response headers from the target URL.

2.  **Analyze Security Headers:**
    * **Action:** Parse the fetched headers (from step 1 output).
    * **Check for presence and correctness of key security headers:**
        * `Strict-Transport-Security` (HSTS)
        * `Content-Security-Policy` (CSP)
        * `X-Content-Type-Options` (e.g., `nosniff`)
        * `X-Frame-Options` (e.g., `DENY`, `SAMEORIGIN`)
        * `X-XSS-Protection`
        * `Referrer-Policy`
        * `Permissions-Policy` (formerly `Feature-Policy`)
    * **Check for potentially revealing headers:**
        * `Server` (e.g., Apache/2.4.52 (Ubuntu))
        * `X-Powered-By` (e.g., PHP/8.1.2)
        * `X-AspNet-Version`
    * **Purpose:** Identify missing security headers or misconfigurations, and note information leakage.

**Storage and Reporting:**

* The raw output from `curl` (all headers) should be saved to:
    `/work_dir/instruments_output/WebAppHeaderCheck/headers_[sanitized_target_url]_[output_tag_if_provided]_[timestamp].txt`
    (Sanitize `target_url` for filename, e.g., replace `http://` and `/` with underscores).
* A summary report in Markdown format should be provided to the user, including:
    * Target URL.
    * Full list of fetched headers.
    * **Security Header Analysis:**
        * List of **present and correctly configured** security headers with their values.
        * List of **missing** key security headers.
        * List of **misconfigured or weak** security headers with their values and why.
    * **Information Leakage:** List any revealing headers like `Server`, `X-Powered-By`, etc., and their values.
    * Note if `-k` (insecure) was used by `curl` due to certificate issues.

**Prompt to Define this Instrument with Agent Zero:**

"Define a new instrument named 'WebAppHeaderCheck'.
This instrument must accept one mandatory argument: 'target_url' (string), and one optional argument: 'output_tag' (string, defaults to 'default_analysis').

The instrument will perform the following sequence of actions:

Execute curl -sSLk -I [target_url] to fetch HTTP/S headers.

Analyze the fetched headers. Specifically check for the presence and configuration of: Strict-Transport-Security, Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, and Permissions-Policy. Also, note any Server, X-Powered-By, or similar information-leaking headers.

The raw headers should be saved to /work_dir/instruments_output/WebAppHeaderCheck/headers_[sanitized_target_url]_[output_tag]_[timestamp].txt.
Provide a Markdown summary detailing the target URL, all fetched headers, a list of present/missing/misconfigured security headers, and any information leakage found. Note if curl used the -k option.
Confirm when 'WebAppHeaderCheck' is defined, listing its arguments."


**Prompt to Use this Instrument:**

"Use the instrument 'WebAppHeaderCheck' for the URL 'https://vulnerable.example.com/test.php' with output_tag 'initial_scan'.
Log outputs and report the summary as defined."