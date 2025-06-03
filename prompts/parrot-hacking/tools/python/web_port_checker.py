```python
# web_port_checker.py
import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

# Enhanced comments and explanations for clarity.

def check_port(ip_address: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
    """
    Checks if a specific port is open on a given IP address using TCP.

    Args:
        ip_address: The target IP address.
        port: The target port number.
        timeout: Connection timeout in seconds.

    Returns:
        A tuple containing (port, is_open, status_message).
        is_open is True if the port is open, False otherwise.
        status_message provides details like 'open', 'closed', or 'error: <reason>'.
    """
    try:
        # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM).
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set a timeout for the connection attempt to avoid long hangs.
            sock.settimeout(timeout)
            # Attempt to connect to the IP address and port.
            # connect_ex returns 0 on success, otherwise an error indicator.
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                return port, True, "open"
            else:
                # Provide a more descriptive reason if possible, though connect_ex error codes can be system-dependent.
                # For simplicity, we'll just say closed or map common errors if needed.
                return port, False, f"closed (errno {result})"
    except socket.timeout:
        return port, False, "closed (timeout)"
    except socket.gaierror as e: # Address info error
        return port, False, f"error (address-related: {e})"
    except socket.error as e:
        # Catch other socket-related errors.
        return port, False, f"error (socket: {e})"
    except Exception as e:
        # Catch any other unexpected errors.
        return port, False, f"error (unexpected: {e})"

def main():
    """
    Main function to parse command-line arguments and check specified or common web ports.
    This script is designed to be callable by Agent Zero.
    """
    parser = argparse.ArgumentParser(
        description="Simple Web Port Checker for Agent Zero. Checks TCP ports.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    parser.add_argument(
        "ip_address",
        help="The target IP address to scan."
    )
    parser.add_argument(
        "--ports",
        nargs='+',
        type=int,
        default=[80, 443, 8000, 8080, 8888], # Added 8888 as another common alternative http port
        help="A list of TCP ports to check (default: 80 443 8000 8080 8888)."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds for each port (default: 1.0)."
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of concurrent threads to use for scanning (default: 10)."
    )

    # If Agent Zero runs this script without arguments (e.g., just after creating it),
    # print usage instructions.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print("\nThis script checks specified or common TCP web ports on a given IP address.")
        print("It can be used by Agent Zero to quickly assess web service availability.")
        print("\nExample (manual execution):")
        print("  python web_port_checker.py 192.168.1.100")
        print("  python web_port_checker.py 192.168.1.100 --ports 80 443 8081 --timeout 0.5 --threads 20")
        sys.exit(1)

    args = parser.parse_args()

    target_ip = args.ip_address
    ports_to_check = sorted(list(set(args.ports))) # Remove duplicates and sort
    timeout = args.timeout
    max_threads = args.threads

    print(f"Initiating TCP port check on {target_ip} for ports: {ports_to_check} (Timeout: {timeout}s, Threads: {max_threads})")

    open_ports_details = []

    # Using ThreadPoolExecutor for concurrent port scanning.
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all port check tasks to the executor.
        future_to_port = {executor.submit(check_port, target_ip, port, timeout): port for port in ports_to_check}

        for future in as_completed(future_to_port):
            port_num, is_open, status_msg = future.result()
            if is_open:
                print(f"  [+] Port {port_num}/tcp is {status_msg} on {target_ip}")
                open_ports_details.append(f"{port_num}/tcp ({status_msg})")
            else:
                # Optionally print closed/error status for verbosity, or keep it quiet.
                # For Agent Zero, it might be better to only report open ports unless full status is requested.
                # print(f"  [-] Port {port_num}/tcp is {status_msg} on {target_ip}")
                pass # Default: only print open ports

    if open_ports_details:
        print(f"\nSummary for {target_ip}:")
        print(f"  Open TCP ports found: {', '.join(open_ports_details)}")
    else:
        print(f"\nSummary for {target_ip}:")
        print(f"  No open TCP ports found among those checked ({ports_to_check}).")

if __name__ == "__main__":
    # This script is intended to be called by Agent Zero.
    # Agent Zero should be prompted to provide the IP address as a command-line argument.
    #
    # Example Agent Zero Prompt:
    # "Create a Python script named 'web_port_checker.py' in '/tools/python/' with the content provided previously.
    # Then, use this script to check common web ports on IP '192.168.1.1'.
    # Specifically, check ports 80, 443, and 8080 with a timeout of 2 seconds and 5 threads.
    # Report the full output of the script."
    #
    # Agent Zero execution command would be like:
    # `python3 /tools/python/web_port_checker.py 192.168.1.1 --ports 80 443 8080 --timeout 2 --threads 5`
    #
    # To make it executable by Agent Zero if it saves it (though not strictly necessary for python scripts):
    # Agent Zero might need to be told: "Ensure the script /tools/python/web_port_checker.py is executable (chmod +x)."
    # However, usually `python3 /path/to/script.py <args>` is sufficient.
    main()
