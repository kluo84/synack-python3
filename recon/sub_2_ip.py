#!/usr/bin/env python3

"""
This script captures the hostname in a file, converts it to IP address, and compares it with the in-scope IP address.
Finally, it generates the in-scope domains list.
"""

import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor

def read_hostnames_from_file(file_path):
    with open(file_path, "r") as file:
        hostnames = file.read().splitlines()
    return hostnames

def hostname_to_ip(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        pass

def compare_ips(hostnames_ips, in_scope_ips_set):
    in_scope_domains = {hostname for hostname, ip in hostnames_ips.items() if ip in in_scope_ips_set}
    return in_scope_domains

def write_in_scope_domains_to_file(file_path, in_scope_domains):
    with open(file_path, "w") as file:
        for domain in in_scope_domains:
            file.write(domain + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input file containing hostnames")
    parser.add_argument("-o", "--output", required=True, help="Output file to store in-scope domains")
    parser.add_argument("-s", "--scope", required=True, help="File containing in-scope IP addresses")
    args = parser.parse_args()

    hostnames = read_hostnames_from_file(args.input)
    in_scope_ips = read_hostnames_from_file(args.scope)

    with ThreadPoolExecutor() as executor:
        hostnames_ips = {hostname: ip for hostname, ip in zip(hostnames, executor.map(hostname_to_ip, hostnames))}
    in_scope_ips_set = set(in_scope_ips)
    in_scope_domains = compare_ips(hostnames_ips, in_scope_ips_set)

    print("Comparing IPs:", end=" ")
    comparison_count = 0
    total_count = len(hostnames_ips)
    for hostname, ip in hostnames_ips.items():
        if ip in in_scope_ips_set:
            comparison_count += 1
        print(f"\rComparing IPs: {comparison_count}/{total_count}", end="")
    print()

    write_in_scope_domains_to_file(args.output, in_scope_domains)
    print(f"In-scope domains have been written to {args.output}")

if __name__ == "__main__":
    main()