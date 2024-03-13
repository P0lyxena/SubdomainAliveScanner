### README.md

```markdown
# SubdomainAliveScanner

SubdomainAliveScanner is a powerful, asynchronous Python tool designed to quickly scan thousands of subdomains, identifying those that are "alive" based on specific HTTP status codes. Utilizing `aiohttp` for non-blocking I/O operations, it offers an efficient way to conduct large-scale subdomain status checks, providing real-time feedback and detailed summaries of scan results.

## Features

- **Asynchronous Scanning:** Leverages Python's `asyncio` and `aiohttp` libraries for fast, non-blocking network requests.
- **Customizable Status Codes:** Users can define which HTTP status codes should be considered as indicating an alive subdomain.
- **Real-Time Progress Updates:** Displays ongoing progress, including the number of subdomains scanned and the last subdomain checked.
- **Error Handling:** Gracefully manages request errors, ensuring the scan continues uninterrupted.
- **Detailed Summary:** Upon completion, reports the total number of alive subdomains found, total scanned, and scan duration.

## Requirements

- Python 3.7+
- `aiohttp`

## Installation

First, ensure you have Python 3.7 or higher installed on your system. Then, install the required `aiohttp` library using pip:

```bash
pip install aiohttp
```

## Usage

1. Prepare a text file named `subdomains.txt` in the same directory as the script. This file should list the subdomains to scan, one per line.
2. Run the script using Python:

```bash
python main.py
```

3. Follow the real-time progress in the terminal. The results will be saved to a timestamped file once the scan completes.

## Customization

To modify which HTTP status codes are considered, edit the `alive_status_codes` list within the script:

```python
alive_status_codes = [200, 500, 404, 403]
```

You can also adjust the maximum number of concurrent requests by changing the `concurrency_limit` variable:

```python
concurrency_limit = 250
```

## Disclaimer

SubdomainAliveScanner is intended for educational and ethical testing purposes only. Users must ensure they have permission to scan the listed subdomains to avoid unauthorized access or network abuse.

