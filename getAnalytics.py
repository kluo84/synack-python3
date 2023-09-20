#!/usr/bin/env python3.8

from synack import synack
from urllib.parse import urlparse

def connect(synack_instance):
    """
    Connect to Synack and perform registration.
    """
    synack_instance.getSessionToken()
    synack_instance.registerAll()
    synack_instance.getAllTargets()

def get_vuln_locations(synack_instance, codename):
    """
    Fetch analytics for a given codename and return a list of vuln_locations' paths.
    """
    analytics_data = synack_instance.getAnalytics(codename)
    if analytics_data is None:
        print(f"No analytics data found for codename: {codename}")
        return []

    # Extract only the path from the vuln_location URL
    return [urlparse(entry['vuln_location']).path for entry in analytics_data if 'vuln_location' in entry]

def main():
    s1 = synack()
    connect(s1)
    
    categories = ["host", "web application", "mobile"]
    new_vuln_locations = []



    for category in categories:
        codenames = s1.getCodenames(category)
        for codename in codenames:
            new_vuln_locations.extend(get_vuln_locations(s1, codename))

    # Read existing wordlist
    with open("./wordlist/synack-wordlist.txt", "r", encoding="utf-8") as file:
        existing_wordlist = file.readlines()

    # Convert existing wordlist to set for faster lookup
    existing_wordlist_set = set(line.strip() for line in existing_wordlist)

    # Add only unique paths that aren't already in the existing wordlist
    for location in new_vuln_locations:
        stripped_location = location.strip().lstrip('/')  # Remove leading slashes
        if stripped_location not in existing_wordlist_set:
            existing_wordlist_set.add(stripped_location)

    # Convert the set to list and sort
    unique_sorted_list = sorted(existing_wordlist_set)

    # Update the wordlist with unique and sorted entries
    with open("./wordlist/synack-wordlist.txt", "w", encoding="utf-8") as file:
        for location in unique_sorted_list:
            file.write(location + "\n")
            
if __name__ == "__main__":
    main()

