import aiohttp  # Import aiohttp for asynchronous HTTP requests.
import asyncio  # Import asyncio for asynchronous programming.
from datetime import datetime, timedelta  # Import datetime for timestamping and timedelta for measuring durations.
import ssl

# When creating the session, disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Define constants for file paths and HTTP status codes.
input_file_path = 'subdomains.txt'  # Path to the input file listing subdomains to scan.
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M')  # Format current datetime for file naming.
output_file_path = f'result_{current_datetime}.txt'  # Generate output file name with current datetime.
alive_status_codes = [
    # Successful Responses
    200,  # OK
    # Redirection Messages
    301,  # Moved Permanently
    302,  # Found
    303,  # See Other
    307,  # Temporary Redirect
    308,  # Permanent Redirect
    # Client Error Responses
    400,  # Bad Request
    401,  # Unauthorized
    403,  # Forbidden
    404,  # Not Found
    # Server Error Responses
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    # Rate Limiting
    429
] # HTTP status codes considered as indicating an "alive" subdomain.
concurrency_limit = 200  # Maximum number of concurrent asynchronous HTTP requests.

async def check_subdomain_status(session, subdomain, index, total):
    for attempt in range(3):  # Attempt the request up to 3 times
        try:
            # Use the session with SSL verification disabled
            response = await session.get(f'http://{subdomain}', ssl=ssl_context)
            if response.status in alive_status_codes:
                print(f"Success for {subdomain} on attempt {attempt + 1}")
                break  # Exit the loop on success
        except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ClientConnectorCertificateError) as e:
            if attempt < 2:
                print(f"Retry {attempt + 1} for {subdomain} due to {e}")
            else:
                print(f"Failed for {subdomain} after 3 attempts. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {subdomain}: {e}")
            break  # Break on unexpected errors to avoid infinite loops

async def run_subdomain_checks(subdomains):
    """
    Initiates and manages the asynchronous checking of each subdomain's status.

    Args:
        subdomains (list): A list of subdomains to scan.
    """
    start_time = datetime.now()  # Record the start time of the scan.
    tasks = []  # Initialize a list to hold tasks for asynchronous execution.
    connector = aiohttp.TCPConnector(limit_per_host=concurrency_limit)  # Configure the TCP connector with a concurrency limit.
    async with aiohttp.ClientSession(connector=connector) as session:  # Create a session for making HTTP requests.
        for index, subdomain in enumerate(subdomains):  # Iterate over the list of subdomains with their indices.
            # Create an asynchronous task for each subdomain check and add it to the list of tasks.
            task = asyncio.create_task(check_subdomain_status(session, subdomain, index, len(subdomains)))
            tasks.append(task)
        
        alive_subdomains = []  # Initialize a list to hold subdomains that are found to be alive.
        for future in asyncio.as_completed(tasks):  # Process tasks as they are completed.
            result = await future  # Await the result of each task.
            if result:  # If a subdomain is found to be alive (not None), add it to the list of alive subdomains.
                alive_subdomains.append(result)
        
        with open(output_file_path, 'w') as file:  # Open the output file for writing.
            for subdomain in alive_subdomains:  # Iterate over the list of alive subdomains.
                file.write(f'{subdomain}\n')  # Write each alive subdomain to the file.
        
        end_time = datetime.now()  # Record the end time of the scan.
        duration = end_time - start_time  # Calculate the duration of the scan.
        # Print a summary of the scan results and the duration.
        print(f'\n\nAlive subdomains have been saved to {output_file_path}.')
        print(f'Found {len(alive_subdomains)} alive subdomains out of {len(subdomains)} in {duration}.')

def main():
    """
    Main function to load subdomains, initiate the scan, and handle asyncio loop.
    """
    # Load subdomains from the input file into a list.
    subdomains = [line.strip() for line in open(input_file_path, 'r')]
    # Print an initial message indicating the start of the scan and the total number of subdomains to be scanned.
    print(f"Starting scan of {len(subdomains)} subdomains...")
    asyncio.run(run_subdomain_checks(subdomains))  # Run the asynchronous subdomain checks.

if __name__ == '__main__':
    main()  # Execute the main function if the script is run directly.
