#!/usr/bin/env python3
import json
import argparse

def generate_urls(input_filename, output_filename):
    # Open the input file and load the JSON data
    with open(input_filename, 'r') as infile:
        data = json.load(infile)
        include_rules = data['target']['scope']['include']

    # Open the output file to write the URLs
    with open(output_filename, 'w') as outfile:
        for item in include_rules:
            if item['enabled']:
                host = item.get('host', '').replace('^', '').replace('$', '')
                port = item.get('port', '').replace('^', '').replace('$', '')
                if port == '80':
                    url = f'http://{host}'
                elif port == '443':
                    url = f'https://{host}'
                else:
                    url = f'http://{host}' # or https://{host} based on your default need
                outfile.write(f'{url}\n')

# Create parser and add arguments
parser = argparse.ArgumentParser(description='Generate URLs from JSON file.')
parser.add_argument('-i', '--input', help='Input JSON filename', required=True)
parser.add_argument('-o', '--output', help='Output filename', required=True)

# Parse the arguments
args = parser.parse_args()

# Call the function with arguments
generate_urls(args.input, args.output)
