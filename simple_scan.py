import socket
import ssl
import argparse
import urllib.request
from bs4 import BeautifulSoup

def check_http_methods(url, timeout=5):
    """Checks for supported HTTP methods (OPTIONS, TRACE, etc.)."""
    try:
        req = urllib.request.Request(url, method='OPTIONS')
        response = urllib.request.urlopen(req, timeout=timeout)
        allowed_methods = response.headers.get('Allow', '')
        print(f"  Allowed Methods: {allowed_methods}")

        # Check for TRACE (potentially dangerous)
        try:
            trace_req = urllib.request.Request(url, method='TRACE')
            trace_response = urllib.request.urlopen(trace_req, timeout=timeout)
            if trace_response.status == 200:
                print("  TRACE enabled (potentially dangerous!)")
        except urllib.error.HTTPError as e:
            if e.code == 405: # Method Not Allowed is expected in many cases
                pass
            else:
                print(f"  TRACE Error: {e}")        

    except urllib.error.URLError as e:
        print(f"  Error checking methods: {e}")
    except socket.timeout:
        print("  Timeout checking methods.")


def check_common_files(url, common_files, timeout=5):
    """Checks for existence of common files/directories."""
    print("\nChecking for common files/directories:")
    for file in common_files:
        full_url = url.rstrip('/') + '/' + file  # Ensure proper slashes
        try:
            response = urllib.request.urlopen(full_url, timeout=timeout)
            if response.status == 200:
                print(f"  Found: {full_url}")
            elif response.status == 403: # Forbidden is still an interesting finding
                print(f"  Forbidden: {full_url}")
        except urllib.error.HTTPError as e:
            if e.code != 404:  # Ignore 404s, we're looking for others
                print(f"  Error checking {full_url}: {e}")
        except socket.timeout:
            print(f"  Timeout checking {full_url}")


def check_x_powered_by(url, timeout=5):
    """Checks for the X-Powered-By header."""
    try:
        response = urllib.request.urlopen(url, timeout=timeout)
        x_powered_by = response.headers.get('X-Powered-By')
        if x_powered_by:
            print(f"\n  X-Powered-By: {x_powered_by}")
        else:
            print("\n  X-Powered-By header not found.")
    except (urllib.error.URLError, socket.timeout) as e:
         print(f"\n  Error checking X-Powered-By: {e}")



def check_for_interesting_strings(url, strings_to_check, timeout=5):
    """Searches for interesting strings in the page source."""
    try:
        response = urllib.request.urlopen(url, timeout=timeout)
        html = response.read().decode('utf-8', errors='ignore')  # Handle encoding
        soup = BeautifulSoup(html, 'html.parser') # Use BeautifulSoup for parsing

        for string in strings_to_check:
            if string in html: #Simple string search first
                print(f"  Found string: {string}")
            # More robust search using BeautifulSoup (e.g., in attributes)
            # Example: check for comments
            comments = soup.find_all(string=lambda text: isinstance(text, str) and string in text)
            for comment in comments:
                print(f"  Found string in comment: {comment}")

    except (urllib.error.URLError, socket.timeout) as e:
        print(f"  Error checking for strings: {e}")



def main():
    parser = argparse.ArgumentParser(description="Simple web vulnerability scanner.")
    parser.add_argument("url", help="The URL to scan (e.g., http://example.com)")
    args = parser.parse_args()

    url = args.url

    common_files = ["admin.php", "login.php", "config.php", "backup.zip", ".git/config", "robots.txt", "sitemap.xml"]  # Extend as needed
    strings_to_check = ["SQL syntax error", "Warning:", "Notice:", "Fatal error:", "deprecated"] # Example strings

    print(f"Scanning: {url}")

    check_http_methods(url)
    check_x_powered_by(url)
    check_common_files(url, common_files)
    check_for_interesting_strings(url, strings_to_check)

if __name__ == "__main__":
    main()
