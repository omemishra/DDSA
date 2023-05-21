import argparse
import hashlib
import re
import subprocess
from urllib.parse import urlparse, unquote
from colorama import Fore
import os

def fetch_data(domain):
    # Fetch domain data using gau
    command = ["gau", domain]
    try:
        output = subprocess.check_output(command, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        exit(1)

    # Remove any scheme prefixes (e.g., "http://", "https://") from the domain
    parsed_domain = urlparse(domain)
    if parsed_domain.scheme:
        domain_name = parsed_domain.netloc
    else:
        domain_name = domain

    # Generate output file name based on the MD5 hash of the domain
    md5_hash = hashlib.md5(unquote(domain_name).encode()).hexdigest()

    output_file = md5_hash

    # Decode the fetched data
    output = unquote(output)

    file_path = output_file

    if os.path.isfile(file_path):
        print("Domain Already Scanned Earlier.")
        print("Domain- "+domain)
        print("Output FIle- "+output_file)
        with open(file_path, "r") as file:
            existing_output = file.read()
            main_function(existing_output)
    else:
        # Write the fetched data to the output file
        with open(output_file, "w") as file:
            file.write(output)

        print(f"Data fetched and stored in '{output_file}'")
        main_function(output)


def search_emails(output):
    print("Emails found:")
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", output)
    filtered_emails = [email for email in emails if not re.search(r"\.(svg|png|jpg|jpeg)\b", email)]
    for email in filtered_emails:
        urls_with_email = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if email in url]
        print(Fore.GREEN + f"Email: {email}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_email))
        print()


def search_sessions(output):
    print("Sessions found:")
    sessions = re.findall(r"\b[A-Fa-f0-9]{64}\b", output)
    for session in sessions:
        urls_with_session = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if session in url]
        print(Fore.GREEN + f"Sessions Found: {session}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_session))
        print()


def search_api_keys(output):
    print("API keys found:")
    apikeys = re.findall(r"\b[A-Za-z0-9]{32}\b", output)
    for key in apikeys:
        urls_with_key = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if key in url]
        print(Fore.GREEN + f"API Key: {key}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_key))
        print()


def search_jwt_tokens(output):
    print("JWT tokens found:")
    jwt_tokens = re.findall(r"eyJh\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b", output)
    for jwt in jwt_tokens:
        urls_with_jwt = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if jwt in url]
        print(Fore.GREEN + f"JWT Token: {jwt}")
        print(Fore.RED + "Found in URL:")
        print("\n".join(urls_with_jwt))
        print()


def search_other_data(output):
    other_data = input("Enter the patterns to search (separated by commas): ")

    patterns = [pattern.strip() for pattern in other_data.split(",")]
    for pattern in patterns:
        print(f"{pattern} found:")
        matches = re.findall(pattern, output, re.IGNORECASE)
        urls_with_pattern = [url for url in re.findall(r"https?://[^\s/$.?#].[^\s]*", output) if any(pattern in url for pattern in matches)]
        if urls_with_pattern:
            print("Found in URLs:")
            print("\n".join(urls_with_pattern))


def process_options(selected_options, output):
    if 1 in selected_options:
        search_emails(output)

    if 2 in selected_options:
        search_sessions(output)

    if 3 in selected_options:
        search_api_keys(output)

    if 4 in selected_options:
        search_jwt_tokens(output)

    if 5 in selected_options:
        search_other_data(output)


def main_function(output):
    print("Select the options to process the fetched data:")
    print("1. Search for emails")
    print("2. Search for sessions")
    print("3. Search for API keys")
    print("4. Search for JWT tokens")
    print("5. Search for other specified data")

    while True:
        # Process the selected options
        selected_options = input("Enter the option numbers (separated by commas), or enter '6' to exit: ")
        selected_options = [int(option) for option in selected_options.split(",")]

        if 6 in selected_options:
            print("Exiting...")
            break

        process_options(selected_options, output)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="The domain to search")
    args = parser.parse_args()

    # Fetch data and get the output file
    fetch_data(args.domain)

