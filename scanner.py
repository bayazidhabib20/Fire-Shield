import base64
import requests
import re
import sys

# Reverse + Base64 encoded key (Masked for security)
ENCODED_REVERSED_KEY = "PT1pYlhOMGFXNW5hVzVwY21WemRHOXBaR2x1WVhSbFpXUmxaRzkw"

def get_actual_key():
    """Decode and reverse back the key at runtime"""
    try:
        decoded_bytes = base64.b64decode(ENCODED_REVERSED_KEY)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str[::-1]
    except Exception:
        return None

def sanitize_url(url):
    """Auto-handle invalid or incomplete URLs"""
    url = url.strip()
    if not url:
        return None
    
    # Add https if missing
    if not re.match(r'^https?://', url):
        url = 'https://' + url
    
    # Standard URL validation regex
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
        r'localhost|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?' 
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if re.match(regex, url):
        return url
    return None

def fire_shield_scanner():
    print("\n" + "="*50)
    print("      FIRE-SHIELD: ADVANCED FORENSIC SCANNER")
    print("="*50)
    
    raw_input = input("\n[?] Enter Target URL: ")
    target_url = sanitize_url(raw_input)
    
    if not target_url:
        print("\n[!] Error: Invalid URL format.")
        return

    api_key = get_actual_key()
    
    headers = {'API-Key': api_key, 'Content-Type': 'application/json'}
    data = {"url": target_url, "visibility": "unlisted"}
    
    try:
        print(f"\n[*] Scanning Target: {target_url}")
        print("[*] Requesting analysis from URLscan.io...")
        
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, json=data)
        
        if response.status_code == 200:
            result_link = response.json().get('result')
            print(f"\n[+] SCAN SUCCESSFUL!")
            print(f"[+] Report URL: {result_link}")
        elif response.status_code == 401:
            print("\n[!] Error: Unauthorized. Please check API Key configuration.")
        else:
            print(f"\n[!] Server Error: HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n[!] Network Error: Please check your internet connection.")
    except Exception as e:
        print(f"\n[!] Unexpected Error: {e}")

if __name__ == "__main__":
    try:
        fire_shield_scanner()
    except KeyboardInterrupt:
        print("\n\n[!] Session interrupted. Exiting...")
        sys.exit()