#!/usr/bin/env python3

import argparse
import concurrent.futures
from OpenSSL import SSL
import idna
from socket import socket

def get_certificate(ip, port):
    # Create context
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.check_hostname = False
    context.verify_mode = SSL.VERIFY_NONE

    # Create OpenSSL connection
    connection = SSL.Connection(context, socket())
    connection.connect((ip, port))

    try:
        connection.do_handshake()
    except SSL.Error as e:
        print(f"Error during handshake: {str(e)}")
        return None

    certificate = connection.get_peer_certificate()
    return certificate

def get_common_name(certificate):
    common_name = certificate.get_subject().CN
    return common_name

def fetch_cert(ip):
    port = 443  # Default HTTPS port
    print(f"Fetching certificate from {ip}:{port}...")
    certificate = get_certificate(ip, port)
    if certificate:
        cn = get_common_name(certificate)
        print(f"  Got CN: {cn}")
        return f"{ip}:{port} - {cn}\n"
    else:
        print(f"  Failed to get certificate from {ip}:{port}")
        return f"{ip}:{port} - Failed to get certificate\n"

def main():
    parser = argparse.ArgumentParser(description="Fetches the Common Name (CN) from SSL certificates given a list of IP addresses.")
    parser.add_argument("ip_file", type=argparse.FileType('r'),
                        help="a file with one IP address per line")
    parser.add_argument("-o", "--output", type=str, default="output.txt",
                        help="the file to write the CNs to (default: output.txt)")
    args = parser.parse_args()

    with open(args.output, "w") as f:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(fetch_cert, [line.strip() for line in args.ip_file]))
            f.writelines(results)
    args.ip_file.close()

if __name__ == "__main__":
    main()

