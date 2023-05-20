import argparse
import hashlib
import re
import subprocess
from urllib.parse import urlparse, unquote
import colorama
from colorama import Fore


# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("domain", help="The domain to search")
args = parser.parse_args()

# Fetch domain data using gau
command = ["gau", args.domain]
try:
    output = subprocess.check_output(command, universal_newlines=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    exit(1)

# Extract domain name from the provided URL
domain_name = urlparse(args.domain).netloc

# Generate output file name based on the MD5 hash of the domain
md5_hash = hashlib.md5(domain_name.encode()).hexdigest()
output_file = f"{md5_hash}.txt"

# Decode the fetched data
output = unquote(output)

# Write the fetched data to the output file
with open(output_file, "w") as file:
    file.write(output)

print(f"Data fetched and stored in '{output_file}'")

print("Select the options to process the fetched data:")
print("1. Search for emails")
print("2. Search for sessions")
print("3. Search for API keys")
print("4. Search for JWT tokens")
print("5. Search for other specified data")

# Process the selected options
selected_options = input("Enter the option numbers (separated by commas): ")
selected_options = [int(option) for option in selected_options.split(",")]

# Read the fetched data from the output file
with open(output_file, "r") as file:
    output = file.read()

# Search for emails
if 1 in selected_options:
    print("Emails found:")
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", output)
    filtered_emails = [email for email in emails if not re.search(r"\.(svg|png|jpg|jpeg)\b", email)]
    for email in filtered_emails:
        urls_with_email = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if email in url]
        print(Fore.GREEN + f"Email: {email}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_email))
        print()

# Search for sessions
if 2 in selected_options:
    print("Sessions found:")
    sessions = re.findall(r"\b[A-Fa-f0-9]{64}\b", output)
    for session in sessions:
        urls_with_session = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if session in url]
        print(Fore.GREEN + f"Sessions Found: {session}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_session))
        print()



# Search for API keys
if 3 in selected_options:
    print("API keys found:")
    apikeys = re.findall(r"\b[A-Za-z0-9]{32}\b", output)
    for key in apikeys:
        urls_with_key = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if key in url]
        print(Fore.GREEN + f"API Key: {key}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_key))
        print()


if 4 in selected_options:
    print("JWT tokens found:")
    jwt_tokens = re.findall(r"eyJh\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b", output)
    for jwt in jwt_tokens:
        urls_with_jwt = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if jwt in url]
        print(Fore.GREEN + f"JWT Token: {jwt}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_jwt))
        print()


if 5 in selected_options:
    other_data = input("Enter the patterns to search (separated by commas): ")
    patterns = [pattern.strip() for pattern in other_data.split(",")]
    for pattern in patterns:
        print(f"{pattern} found:")
        matches = re.findall(pattern, output, re.IGNORECASE)
        urls_with_pattern = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if any(pattern in url for pattern in matches)]
        if urls_with_pattern:
            print("Found in URLs:")
            print("\n".join(urls_with_pattern))






