#!/usr/bin/env python3.8

import os
import sys
import subprocess
import threading

# Global semaphore to allow 3 threads at a time
semaphore = threading.Semaphore(3)

def run_ffuf(domain):
    with semaphore:
        # Strip 'https://' or 'http://' from the domain for the filename
        clean_domain = domain.replace('http://', '').replace('https://', '')

        # Set an output filename based on the clean domain
        output_file = f"{clean_domain}_ffuf_results.txt"

        # Run ffuf against the domain and write the results to the domain-specific output file
        cmd = [
            "ffuf",
            "-u", f"{domain}/FUZZ",
            "-w", os.path.expanduser("~/Tools/synack-python3/wordlist/synack-wordlist.txt"),
            "--mc=200", "--fl=1", "-o", output_file, "-of", "csv"
        ]
        subprocess.run(cmd)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/domains.txt")
        sys.exit(1)

    input_file = sys.argv[1]

    # Ensure the provided file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(2)

    # Read each domain from the file
    with open(input_file, 'r') as f:
        domains = [line.strip() for line in f]

    # Create threads for each domain
    threads = []
    for domain in domains:
        thread = threading.Thread(target=run_ffuf, args=(domain,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()