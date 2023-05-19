# Domain Data Search and Analysis Tool

The Domain Data Search and Analysis Tool is a powerful command-line utility designed to fetch and analyze data associated with a given domain. It provides a comprehensive set of features to gather valuable information from various sources and perform targeted searches for emails, sessions, API keys, and custom patterns.

## Key Features

- **Data Fetching**: Utilizes the "gau" command-line tool to fetch domain data from different sources, providing a rich dataset for analysis.
- **Data Storage**: Stores the fetched data in a file named after the MD5 hash of the domain, ensuring uniqueness and integrity.
- **URL Decoding**: Decodes URL-encoded data within the fetched results, enabling accurate analysis of the extracted information.
- **Email Extraction**: Searches and identifies email addresses within the fetched data, excluding emails with invalid file extensions such as .svg, .png, .jpg, or .jpeg.
- **Session Identification**: Identifies sessions using a pattern matching approach, extracting session tokens or identifiers from the fetched data.
- **API Key Detection**: Detects API keys using a regex-based search, allowing the identification of sensitive information associated with the domain.
- **Custom Pattern Search**: Enables users to define and search for custom patterns within the fetched data, providing flexibility for targeted analysis.
- **Path Inclusion**: Displays the full URL path where each email is found, allowing users to identify the specific context of email occurrences.

## Installation Guide

$ go install github.com/lc/gau/v2/cmd/gau@latest

pip install -r requirements.txt

## Usage

To use the Domain Data Search and Analysis Tool, follow these steps:

1. Clone the repository.
2. Install the required dependencies.
3. Run the script with the desired domain as an argument.
4. Select the options to process the fetched data.
5. View the results for each selected option.

For detailed instructions on installation and usage, refer to the [User Guide](user-guide.md).

## Contributing

Contributions are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
