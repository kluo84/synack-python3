#!/usr/bin/env python3

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
    all_vuln_locations = []

    for category in categories:
        codenames = s1.getCodenames(category)
        for codename in codenames:
            all_vuln_locations.extend(get_vuln_locations(s1, codename))

    # Read existing wordlist
    with open("./wordlist/synack-wordlist.txt", "r", encoding="utf-8") as file:
        existing_wordlist = file.readlines()

    # Append new paths to the wordlist
    all_vuln_locations.extend(existing_wordlist)

    # Remove duplicates and sort
    unique_sorted_list = sorted(set(all_vuln_locations))

    # Update the wordlist with unique and sorted entries
    with open("./wordlist/synack-wordlist.txt", "w", encoding="utf-8") as file:
        for location in unique_sorted_list:
            file.write(location.strip() + "\n")

if __name__ == "__main__":
    main()
