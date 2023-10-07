#!/usr/bin/env python3
import json
import argparse
import re  # Importing the regular expression library


def extract_unique_hosts(input_filename, output_filename):
    # Open the input file and load the JSON data
    with open(input_filename, 'r') as infile:
        data = json.load(infile)
        include_rules = data['target']['scope']['include']

    # Use a set to store unique hostnames
    unique_hosts = set()

    for item in include_rules:
        if item['enabled']:
            # Using regular expression to clean the host name by removing unwanted characters
            host = item.get('host', '')
            clean_host = re.sub(r'[^a-zA-Z0-9.]+', '', host)  # Keeping only alphanumeric characters and dots
            unique_hosts.add(clean_host)

    # Open the output file to write the unique hostnames
    with open(output_filename, 'w') as outfile:
        for host in unique_hosts:
            outfile.write(f'{host}\n')


# Create parser and add arguments
parser = argparse.ArgumentParser(description='Extract unique host names from JSON file.')
parser.add_argument('-i', '--input', help='Input JSON filename', required=True)
parser.add_argument('-o', '--output', help='Output filename', required=True)

# Parse the arguments
args = parser.parse_args()

# Call the function with arguments
extract_unique_hosts(args.input, args.output)


