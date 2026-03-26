import base64
import requests
import re
import sys
import os

# ─── ANSI Color Codes ─────────────────────────────────────────────────────────
RED    = '\033[91m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
CYAN   = '\033[96m'
RESET  = '\033[0m'

# ─── Reverse-Base64 Masked API Key (DO NOT MODIFY) ────────────────────────────
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

    if not re.match(r'^https?://', url):
        url = 'https://' + url

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

# ─── ASCII Banner ─────────────────────────────────────────────────────────────
BANNER = f"""
{YELLOW}  ______ ___ ____  _____        
 |  ___|_ _| __ \| ____|       
 | |_   | ||   / |  _|         
 |  _|  | || |\ \| |___        
 |_|   |___|_| \_\_____|       
  ____  _   _ ___ ___ _    ____ 
 / ___|| | | |_ _| __| |  |  _ \\
 \___ \| |_| || || _|| |__| | | |
  ___) |  _  || || |___  _| |_| |
 |____/|_| |_|___|_____|_||____/ {RESET}
                    {RED}Version : 1.0.0{RESET}
"""

# ─── Menu ─────────────────────────────────────────────────────────────────────
def show_menu():
    os.system('clear')
    print(BANNER)
    print(f"{GREEN}[-] Tool Created by FIRE-SHIELD{RESET}\n")
    print(f"{GREEN}[::] Select A Scan Module [::]  {RESET}\n")
    print(f"  {RED}[01]{RESET}  {GREEN}Scan URL{RESET}")
    print(f"  {RED}[02]{RESET}  {GREEN}Scan File{RESET}")
    print(f"  {RED}[03]{RESET}  {GREEN}Scan IP Address{RESET}")
    print(f"  {RED}[04]{RESET}  {GREEN}Scan Port{RESET}")
    print()
    print(f"  {RED}[99]{RESET}  {GREEN}Exit{RESET}")
    print()
    choice = input(f"{GREEN}[-] Select an option : {RESET}")
    return choice.strip()

# ─── Module 01 : URL Scanner ──────────────────────────────────────────────────
def scan_url():
    os.system('clear')
    print(BANNER)
    print(f"{GREEN}[::] URL SCAN MODULE [::]  {RESET}\n")

    raw_input = input(f"{GREEN}[?] Enter Target URL: {RESET}")
    target_url = sanitize_url(raw_input)

    if not target_url:
        print(f"\n{RED}[!] Error: Invalid URL format.{RESET}")
        input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")
        return

    api_key = get_actual_key()
    headers = {'API-Key': api_key, 'Content-Type': 'application/json'}
    data = {"url": target_url, "visibility": "unlisted"}

    try:
        print(f"\n{YELLOW}[*] Scanning Target: {target_url}{RESET}")
        print(f"{YELLOW}[*] Requesting analysis from URLscan.io...{RESET}")

        response = requests.post(
            'https://urlscan.io/api/v1/scan/',
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            result_link = response.json().get('result')
            print(f"\n{GREEN}[+] SCAN SUCCESSFUL!{RESET}")
            print(f"{GREEN}[+] Report URL: {result_link}{RESET}")
        elif response.status_code == 401:
            print(f"\n{RED}[!] Error: Unauthorized. Please check API Key configuration.{RESET}")
        else:
            print(f"\n{RED}[!] Server Error: HTTP {response.status_code}{RESET}")

    except requests.exceptions.ConnectionError:
        print(f"\n{RED}[!] Network Error: Please check your internet connection.{RESET}")
    except Exception as e:
        print(f"\n{RED}[!] Unexpected Error: {e}{RESET}")

    input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")

# ─── Modules 02-04 : Placeholders ─────────────────────────────────────────────
def coming_soon(module_name):
    os.system('clear')
    print(BANNER)
    print(f"{YELLOW}[*] {module_name} module is under construction.{RESET}\n")
    print(f"{RED}[!] This feature will be available in a future update.{RESET}")
    input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")

# ─── Main Loop ────────────────────────────────────────────────────────────────
def main():
    while True:
        try:
            choice = show_menu()

            if choice == '01':
                scan_url()
            elif choice == '02':
                coming_soon("File Scan")
            elif choice == '03':
                coming_soon("IP Address Scan")
            elif choice == '04':
                coming_soon("Port Scan")
            elif choice == '99':
                os.system('clear')
                print(f"\n{RED}[!] Exiting FIRE-SHIELD. Stay Safe.{RESET}\n")
                sys.exit()

        except KeyboardInterrupt:
            os.system('clear')
            print(f"\n{RED}[!] Session interrupted. Exiting...{RESET}\n")
            sys.exit()

if __name__ == "__main__":
    main()
