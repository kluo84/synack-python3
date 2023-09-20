#!/bin/bash

# Check if a file path was provided
if [[ -z "$1" ]]; then
    echo "Usage: $0 /path/to/domains.txt"
    exit 1
fi

# Input file from the command line argument
input_file="$1"

# Ensure the provided file exists
if [[ ! -f "$input_file" ]]; then
    echo "Error: File '$input_file' does not exist."
    exit 2
fi

# Read each domain from the file
while IFS= read -r domain; do
    # Strip 'https://' or 'http://' from the domain for the filename
    clean_domain=${domain#http://}
    clean_domain=${clean_domain#https://}

    # Set an output filename based on the clean domain
    output_file="${clean_domain}_ffuf_results.txt"
   
    # Run ffuf against the domain and write the results to the domain-specific output file
    ffuf -u "$domain/FUZZ" -w ~/Tools/synack-python3/wordlist/synack-wordlist.txt --mc=200 --fl=1 -o $output_file -of csv
done < "$input_file"