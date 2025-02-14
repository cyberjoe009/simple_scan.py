# simple_scan.py
Similar to nikto

How to Use:

1) Save: Save the code as a Python file (e.g., simple_scanner.py).

2) Install BeautifulSoup: pip install beautifulsoup4

3) Run: Execute the script from the command line:
   ( python simple_scanner.py http://example.com )

   (replace
   http://example.com with the URL you want to scan).
    
______________________________________________________________________________________________________

Important Considerations:

1) Ethical Use: Use this tool responsibly and only on websites that you have permission to scan. Unauthorized 
   scanning is illegal and unethical.

2) Limitations: This is a very basic scanner. Real-world vulnerability scanners like Nikto are much more 
   complex and have databases of thousands of vulnerabilities. This script is a starting point for learning.

3) False Positives: Be aware that this script (and even professional scanners) can produce false positives.

4) Always manually verify any potential vulnerabilities.

5) Further Development: To make this a more useful tool, you could add features like:

   Plugin system for different vulnerability checks.

   More sophisticated HTML parsing.

   Support for different HTTP methods (POST, PUT, DELETE, etc.).

   Output to different formats (e.g., CSV, JSON).

   SSL certificate checking.

   Handling redirects.

   ______________________________________________________________________________________________________

                              Improvements and explanations:

*Error Handling: Includes try...except blocks to handle common errors like URL errors, timeouts, and HTTP errors (like 404 Not Found). This makes the script more robust. It also specifically handles the 405 Method Not Allowed error, which is expected for some HTTP method checks.

*Timeout: Adds a timeout parameter to urllib.request.urlopen() to prevent the script from hanging indefinitely if a server is unresponsive.

*HTTP Method Checking (OPTIONS, TRACE): Implements checking for allowed HTTP methods using the OPTIONS request. Critically, it now checks for the TRACE method, which can be a security risk.

*Common Files: Provides a list of common files/directories to check for. You should expand this list! It now correctly handles slashes in URLs. It also checks for 403 Forbidden responses, as these can be just as 
interesting as 200 OK.

*X-Powered-By Header: Checks for the X-Powered-By header, which can reveal information about the server.

*String Searching: Implements a function to search for interesting strings (like error messages) in the page source. Uses BeautifulSoup to parse the HTML, making the search for strings more robust (it can now search inside HTML comments or tags more reliably). It also handles potential encoding issues when reading the HTML.

*BeautifulSoup: Uses BeautifulSoup for parsing the HTML content, which is much more reliable than just string searching, especially when you want to look within specific HTML elements, attributes, or comments.

*Clearer Output: Improved the output formatting to make it easier to read.

*Command-Line Arguments: Uses argparse to take the URL as a command-line argument, making the script more user-friendly.

*Comments: Added more comments to explain the code.
