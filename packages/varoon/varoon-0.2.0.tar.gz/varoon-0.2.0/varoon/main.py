#!/usr/bin/env python3
'''
Author: R0X4R (Eshan Singh)
Version: 0.2.0
'''

import aiohttp
import asyncio
import sys
from urllib.parse import urlparse, urlencode, parse_qs

# Asynchronous function to check if any query parameters are reflected in the response body
async def check_reflected(session, url):
    reflected_params = []

    try:
        # Send a GET request to the URL with a timeout of 10 seconds
        async with session.get(url, timeout=10) as response:
            # If the response is a redirect, return an empty list
            if response.status >= 300 and response.status < 400:
                return reflected_params

            # Check if the response content type is HTML
            content_type = response.headers.get("Content-Type", "")
            if "html" not in content_type:
                return reflected_params

            # Read the response body as text
            body = await response.text()
            # Parse the URL to extract query parameters
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)

            # Check if any query parameter values are reflected in the response body
            for key, values in query_params.items():
                for value in values:
                    if value in body:
                        reflected_params.append(key)

    except aiohttp.ClientError:
        pass

    return reflected_params

# Asynchronous function to check if appending a suffix to a query parameter value is reflected in the response body
async def check_append(session, url, param, suffix):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # If the parameter is not in the query parameters, return False
    if param not in query_params:
        return False

    # Append the suffix to the parameter value
    query_params[param] = query_params[param][0] + suffix
    # Update the URL with the modified query parameters
    updated_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

    # Check if the modified parameter value is reflected in the response body
    reflected = await check_reflected(session, updated_url)
    return param in reflected

# Asynchronous function to process a single URL
async def process_url(session, url, semaphore):
    async with semaphore:
        # Check if any query parameters are reflected in the response body
        reflected_params = await check_reflected(session, url)
        if not reflected_params:
            return

        for param in reflected_params:
            # Check if appending "test1234" to the parameter value is reflected in the response body
            if await check_append(session, url, param, "test1234"):
                dangerous_chars = ['"', '<', '>', '$', '|', '(', ')', '`', ':', ';', '{', '}']
                output = [url, param]
                for char in dangerous_chars:
                    # Check if appending dangerous characters to the parameter value is reflected in the response body
                    if await check_append(session, url, param, f"aprefix{char}asuffix"):
                        output.append(char)

                # If any dangerous characters are reflected, print the URL, parameter, and characters
                if len(output) > 2:
                    print(f"URL: {output[0]} Param: [ {output[1]} ] Unfiltered: [ {' '.join(output[2:])} ]")

# Asynchronous function to process a list of URLs
async def process_urls(urls):
    semaphore = asyncio.Semaphore(50)  # Increased the semaphore limit for more concurrency
    # Create an aiohttp session with a custom User-Agent header
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}) as session:
        # Create a list of tasks to process each URL
        tasks = [process_url(session, url, semaphore) for url in urls]
        # Run the tasks concurrently
        await asyncio.gather(*tasks)

# Function to read URLs from stdin
def read_urls_from_stdin():
    # Read lines from stdin and strip extra spaces
    urls = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return urls

# Main function that reads from stdin and processes the URLs
def main():
    # Read URLs from stdin
    urls = read_urls_from_stdin()

    # Check if there are any URLs to process
    if not urls:
        print("No URLs to process. Please provide URLs via stdin or pipe them into varoon.")
        return

    # Run the process_urls function with the list of URLs
    asyncio.run(process_urls(urls))

if __name__ == "__main__":
    main()
