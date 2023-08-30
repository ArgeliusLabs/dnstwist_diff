import os
import json
import time
import requests

# Set your domains
DOMAINS = ['argeliuslabs.com', 'example.com']

# Slack webhook URL
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/XXXXXXXXXX/#############/*****************'

# Time to wait between each domain in seconds (900 seconds = 15 minutes)
WAIT_TIME = 60

for DOMAIN in DOMAINS:
    # Run dnstwist and save the results to a json file
    os.system(f'dnstwist {DOMAIN} -r -f json > dnstwist_results_{DOMAIN}.json')

    # Load the current and previous results
    try:
        with open(f'dnstwist_results_{DOMAIN}.json') as f:
            current_results = json.load(f)
    except FileNotFoundError:
        current_results = []

    try:
        with open(f'dnstwist_results_{DOMAIN}_prev.json') as f:
            prev_results = json.load(f)
    except FileNotFoundError:
        prev_results = []

    # Compare the results and print new domains and their DNS information
    current_domains = [result['domain'] for result in current_results]
    prev_domains = [result['domain'] for result in prev_results]

    new_results = [result for result in current_results if result['domain'] not in prev_domains]

    if new_results:
        message = f'New dnstwist results for {DOMAIN}:\n'
        for result in new_results:
            message += json.dumps(result, indent=4) + '\n'
    else:
        message = f'No new dnstwist results for {DOMAIN}.'

    print(message)

    # Send the message to Slack
    requests.post(SLACK_WEBHOOK_URL, json={'text': message})

    # Save the current results for comparison next time
    with open(f'dnstwist_results_{DOMAIN}_prev.json', 'w') as f:
        json.dump(current_results, f)

    # Wait before processing the next domain
    if DOMAIN != DOMAINS[-1]:
        time.sleep(WAIT_TIME)
