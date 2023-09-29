#!/usr/bin/env python3
import json
import argparse
import re  # Importing the regular expression library


def extract_hosts(input_filename, output_filename):
    # Open the input file and load the JSON data
    with open(input_filename, 'r') as infile:
        data = json.load(infile)
        include_rules = data['target']['scope']['include']

    # Open the output file to write the hostnames
    with open(output_filename, 'w') as outfile:
        for item in include_rules:
            if item['enabled']:
                # Using regular expression to clean the host name by removing unwanted characters
                host = item.get('host', '')
                clean_host = re.sub(r'[^a-zA-Z0-9.]+', '', host)  # Keeping only alphanumeric characters and dots
                outfile.write(f'{clean_host}\n')


# Create parser and add arguments
parser = argparse.ArgumentParser(description='Extract host names from JSON file.')
parser.add_argument('-i', '--input', help='Input JSON filename', required=True)
parser.add_argument('-o', '--output', help='Output filename', required=True)

# Parse the arguments
args = parser.parse_args()

# Call the function with arguments
extract_hosts(args.input, args.output)

