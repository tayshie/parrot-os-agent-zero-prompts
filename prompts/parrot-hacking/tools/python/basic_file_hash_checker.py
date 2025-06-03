# basic_file_hash_checker.py
import hashlib
import argparse
import sys
import os

def calculate_hashes(file_path: str) -> dict:
    """
    Calculates MD5, SHA1, SHA256, and SHA512 hashes for a given file.

    Args:
        file_path: Path to the file.

    Returns:
        A dictionary containing the hashes { 'md5': '...', 'sha1': '...', ... }
        Returns None if the file cannot be read.
    """
    hashes = {}
    try:
        with open(file_path, 'rb') as f:
            md5_hash = hashlib.md5()
            sha1_hash = hashlib.sha1()
            sha256_hash = hashlib.sha256()
            sha512_hash = hashlib.sha512()

            while chunk := f.read(8192): # Read in 8KB chunks
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)
                sha512_hash.update(chunk)

            hashes['md5'] = md5_hash.hexdigest()
            hashes['sha1'] = sha1_hash.hexdigest()
            hashes['sha256'] = sha256_hash.hexdigest()
            hashes['sha512'] = sha512_hash.hexdigest()
            return hashes
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        return None
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred with file '{file_path}': {e}", file=sys.stderr)
        return None

def main():
    """
    Main function to parse arguments and calculate/compare file hashes.
    """
    parser = argparse.ArgumentParser(
        description="Basic File Hash Checker for Agent Zero. Calculates MD5, SHA1, SHA256, SHA512.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "file_path",
        help="The path to the file for which to calculate hashes."
    )
    parser.add_argument(
        "--compare_md5",
        type=str,
        default=None,
        help="An MD5 hash to compare against the calculated MD5."
    )
    parser.add_argument(
        "--compare_sha256",
        type=str,
        default=None,
        help="A SHA256 hash to compare against the calculated SHA256."
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print("\nThis script calculates various cryptographic hashes for a given file.")
        print("It can also compare calculated MD5 or SHA256 hashes against provided values.")
        print("Useful for verifying file integrity.")
        print("\nExample (manual execution):")
        print("  python basic_file_hash_checker.py /path/to/somefile.zip")
        print("  python basic_file_hash_checker.py document.pdf --compare_md5 <expected_md5_hash>")
        sys.exit(1)

    args = parser.parse_args()
    file_path = args.file_path

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(file_path):
        print(f"Error: Path '{file_path}' is not a file.", file=sys.stderr)
        sys.exit(1)


    print(f"Calculating hashes for file: '{file_path}'")
    calculated_hashes = calculate_hashes(file_path)

    if calculated_hashes:
        print(f"  MD5   : {calculated_hashes['md5']}")
        print(f"  SHA1  : {calculated_hashes['sha1']}")
        print(f"  SHA256: {calculated_hashes['sha256']}")
        print(f"  SHA512: {calculated_hashes['sha512']}")

        if args.compare_md5:
            print(f"\nComparing provided MD5: {args.compare_md5}")
            if args.compare_md5.lower() == calculated_hashes['md5'].lower():
                print("  MD5 hashes MATCH.")
            else:
                print("  MD5 hashes DO NOT MATCH.")

        if args.compare_sha256:
            print(f"\nComparing provided SHA256: {args.compare_sha256}")
            if args.compare_sha256.lower() == calculated_hashes['sha256'].lower():
                print("  SHA256 hashes MATCH.")
            else:
                print("  SHA256 hashes DO NOT MATCH.")
    else:
        print("Failed to calculate hashes.")

if __name__ == "__main__":
    # Example Agent Zero Prompt:
    # "Create a Python script named 'basic_file_hash_checker.py' in '/tools/python/' with the provided content.
    # Then, use this script to calculate all hashes for the file '/work_dir/downloads/important_tool.exe'.
    # Also, compare its MD5 hash against 'expected_md5_value_here'.
    # Report the full output."
    #
    # Agent Zero execution command:
    # `python3 /tools/python/basic_file_hash_checker.py /work_dir/downloads/important_tool.exe --compare_md5 expected_md5_value_here`
    main()
