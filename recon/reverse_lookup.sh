#!/bin/bash

# Check if input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <ip_list_file>"
    exit 1
fi

# Check if dig command is available
if ! command -v dig &> /dev/null; then
    echo "dig command not found. Please install dnsutils."
    exit 1
fi

# Temporary file to store domains
temp_domain_file="temp_domains.txt"
# File to store unique and sorted domains
final_domain_file="final_domains.txt"

# Empty previous results if any
> "$temp_domain_file"
> "$final_domain_file"

while read -r ip; do
    # Reverse lookup
    domain=$(dig +short -x "$ip")

    if [ -n "$domain" ]; then
        # Remove trailing dot
        domain=${domain%.}

        # Extract domain and write to temp file
        echo "$domain" | awk -F. '{if (NF > 1) print $(NF-1) "." $NF}' >> "$temp_domain_file"
    fi
done < "$1"

# Sort and get unique results
sort "$temp_domain_file" | uniq > "$final_domain_file"

echo "Unique and sorted domains written to $final_domain_file"

# Optional: Remove the temporary file
rm "$temp_domain_file"
