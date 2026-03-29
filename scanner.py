import base64
import requests
import re
import sys
import os
import time
import threading

# ─── ANSI Color Codes ─────────────────────────────────────────────────────────
RED    = '\033[91m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
WHITE  = '\033[97m'
CYAN   = '\033[96m'
RESET  = '\033[0m'

# ─── Reverse-Base64 Masked API Keys (DO NOT MODIFY) ───────────────────────────
_VT_MASKED  = "YzU5MGE0NjY1ODRkMTNlNmZiZjllOGIxNzdiMzlhYzlmNTg3ZmE0Yzk1Y2Q3MThjZjYwZjRlMjdlM2ZkN2Q1Nw=="
_URL_MASKED = "NmQ1NTMyZjIwZDIyLTZhZmItOTY0Ny0xM2NlLWMzNWZjOTEw"

def _decode_key(masked):
    try:
        decoded = base64.b64decode(masked).decode('utf-8')
        return decoded[::-1]
    except Exception:
        return None

def get_vt_key():
    return _decode_key(_VT_MASKED)

def get_url_key():
    return _decode_key(_URL_MASKED)

# ─── URL Sanitizer ────────────────────────────────────────────────────────────
def sanitize_url(url):
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

# ─── ASCII Art Lines (raw, no color) ─────────────────────────────────────────
ASCII_LINES = [
    r"  ______ ___ ____  _____        ",
    r" |  ___|_ _| __ \| ____|       ",
    r" | |_   | ||   / |  _|         ",
    r" |  _|  | || |\ \| |___        ",
    r" |_|   |___|_| \_\_____|       ",
    r"  ____  _   _ ___ ___ _    ____ ",
    r" / ___|| | | |_ _| __| |  |  _ \ ",
    r" \___ \| |_| || || _|| |__| | | |",
    r"  ___) |  _  || || |___  _| |_| |",
    r" |____/|_| |_|___|_____|_||____/ ",
]

WIDTH = 58

# ─── Animated Banner (runs once at startup) ───────────────────────────────────
def banner():
    credit  = "[-] Tool Created by Bayazid Habib [-]"
    version = "Version : 0.1"
    flame_frames = [YELLOW, RED, YELLOW, RED, YELLOW, RED]

    for base_color in flame_frames:
        os.system('clear')
        print()
        for i, line in enumerate(ASCII_LINES):
            color = YELLOW if i % 2 == 0 else RED
            if base_color == RED:
                color = RED if i % 2 == 0 else YELLOW
            print(color + line.center(WIDTH) + RESET)
        print()
        print(GREEN + credit.center(WIDTH)  + RESET)
        print(WHITE + version.center(WIDTH) + RESET)
        print()
        time.sleep(0.2)

    # Final settled frame
    os.system('clear')
    print()
    for line in ASCII_LINES:
        print(YELLOW + line.center(WIDTH) + RESET)
    print()
    print(GREEN + credit.center(WIDTH)  + RESET)
    print(WHITE + version.center(WIDTH) + RESET)
    print()
    time.sleep(0.4)

# ─── Static Banner (used by menu & modules) ───────────────────────────────────
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
                    {RED}Version : 0.1{RESET}
"""

# ─── Menu ─────────────────────────────────────────────────────────────────────
def show_menu():
    os.system('clear')
    print(BANNER)
    print(f"{GREEN}[-] Tool Created by Bayazid Habib [-]{RESET}\n")
    print(f"{GREEN}[::] Select A Scan Module [::]  {RESET}\n")
    print(f"  {RED}[01]{RESET}  {GREEN}Scan URL{RESET}")
    print(f"  {RED}[02]{RESET}  {GREEN}Scan File{RESET}")
    print(f"  {RED}[03]{RESET}  {GREEN}Scan IP Address{RESET}")
    print()
    print(f"  {RED}[99]{RESET}  {GREEN}Exit{RESET}")
    print()
    choice = input(f"{GREEN}[-] Select an option : {RESET}")
    return choice.strip()

# ─── Helper: VirusTotal verdict display ───────────────────────────────────────
def _display_vt_stats(stats, label="Analysis"):
    malicious   = stats.get('malicious', 0)
    suspicious  = stats.get('suspicious', 0)
    harmless    = stats.get('harmless', 0)
    undetected  = stats.get('undetected', 0)
    total       = malicious + suspicious + harmless + undetected

    print(f"\n{CYAN}  ── VirusTotal {label} ──{RESET}")
    print(f"  {GREEN}[+] Harmless   : {harmless}{RESET}")
    print(f"  {YELLOW}[~] Suspicious : {suspicious}{RESET}")
    print(f"  {WHITE}[-] Undetected : {undetected}{RESET}")
    print(f"  {RED}[x] Malicious  : {malicious}{RESET}")

    if malicious == 0 and suspicious == 0:
        print(f"\n{GREEN}[v] Verdict: No significant threats detected ({total} engines checked).{RESET}")
    elif malicious <= 3:
        print(f"\n{YELLOW}[~] Verdict: Low-level flags found. Proceed with caution.{RESET}")
    else:
        print(f"\n{RED}[!] Verdict: Threat detected by {malicious} engine(s). Avoid this target.{RESET}")

# ─── Helper: Detailed per-engine file report (File Scan only) ────────────────
def _display_vt_file_report(attrs, analysis_id, scan_type='file', start_n=1):
    stats      = attrs.get('stats', {})
    results    = attrs.get('results', {})
    malicious  = stats.get('malicious', 0)
    suspicious = stats.get('suspicious', 0)
    harmless   = stats.get('harmless', 0)
    undetected = stats.get('undetected', 0)
    total      = malicious + suspicious + harmless + undetected
    detections = malicious + suspicious

    scan_link  = f"https://www.virustotal.com/gui/{scan_type}-analysis/{analysis_id}"
    SEP        = f"{CYAN}  {'─' * 44}{RESET}"

    # ── Summary header ─────────────────────────────────────────────────────────
    print(f"\n{SEP}")
    det_color = RED if detections > 0 else GREEN
    det_label = f"[!]" if detections > 0 else "[v]"
    print(f"  {det_color}{det_label} Total Detections : {detections} / {total}{RESET}")
    print(f"  {GREEN}[+] Scan Link        : {scan_link}{RESET}")
    print(SEP)

    # ── Bucket engines by category ─────────────────────────────────────────────
    flagged_mal  = {}
    flagged_sus  = {}
    clean        = {}

    for engine, data in results.items():
        cat = data.get('category', '')
        if cat in ('malicious', 'phishing'):
            flagged_mal[engine] = data
        elif cat == 'suspicious':
            flagged_sus[engine] = data
        else:
            clean[engine] = data

    # ── Print flagged: malicious / phishing ────────────────────────────────────
    n = start_n
    if flagged_mal:
        print(f"\n{RED}  ── Malicious / Phishing ──{RESET}")
        for engine in sorted(flagged_mal):
            result = flagged_mal[engine].get('result') or 'Malicious'
            print(f"  {RED}[!] {n}. {engine:<24} -----> {result}{RESET}")
            n += 1

    # ── Print flagged: suspicious ──────────────────────────────────────────────
    if flagged_sus:
        print(f"\n{YELLOW}  ── Suspicious ──{RESET}")
        for engine in sorted(flagged_sus):
            result = flagged_sus[engine].get('result') or 'Suspicious'
            print(f"  {YELLOW}[~] {n}. {engine:<24} -----> {result}{RESET}")
            n += 1

    # ── Print clean engines ────────────────────────────────────────────────────
    if clean:
        print(f"\n{GREEN}  ── Clean / Undetected ──{RESET}")
        for engine in sorted(clean):
            result = clean[engine].get('result') or clean[engine].get('category', 'Clean').capitalize()
            print(f"  {WHITE}[-] {n}. {engine:<24} -----> {result}{RESET}")
            n += 1

    # ── Overall verdict ────────────────────────────────────────────────────────
    print(f"\n{SEP}")
    if detections == 0:
        print(f"  {GREEN}[v] Verdict: Clean. No threats detected ({total} engines).{RESET}")
    elif malicious <= 3:
        print(f"  {YELLOW}[~] Verdict: Low-level flags. Proceed with caution.{RESET}")
    else:
        print(f"  {RED}[!] Verdict: Threat detected by {malicious} engine(s). Avoid this file.{RESET}")
    print(SEP)

# ─── Module 01 : URL Scanner (URLscan.io + VirusTotal) ────────────────────────
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

    # ── Submit both APIs ───────────────────────────────────────────────────────
    print(f"\n{YELLOW}[*] Submitting to URLscan.io and VirusTotal simultaneously...{RESET}")

    urlscan_uuid      = None
    urlscan_submitted = False
    vt_analysis_id    = None
    vt_submitted      = False

    # URLscan.io submission
    try:
        url_resp = requests.post(
            'https://urlscan.io/api/v1/scan/',
            headers={'API-Key': get_url_key(), 'Content-Type': 'application/json'},
            json={"url": target_url, "visibility": "unlisted"},
            timeout=15
        )
        if url_resp.status_code == 200:
            urlscan_uuid      = url_resp.json().get('uuid')
            urlscan_submitted = True
            print(f"{GREEN}[+] URLscan.io : Submitted (UUID: {urlscan_uuid}){RESET}")
        elif url_resp.status_code == 401:
            print(f"{RED}[!] URLscan.io : Unauthorized.{RESET}")
        else:
            print(f"{RED}[!] URLscan.io : HTTP {url_resp.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[!] URLscan.io : Submission error — {e}{RESET}")

    # VirusTotal submission
    try:
        vt_headers = {'x-apikey': get_vt_key()}
        vt_resp = requests.post(
            'https://www.virustotal.com/api/v3/urls',
            headers=vt_headers,
            data={'url': target_url},
            timeout=15
        )
        if vt_resp.status_code == 200:
            vt_analysis_id = vt_resp.json().get('data', {}).get('id', '')
            vt_submitted   = True
            print(f"{GREEN}[+] VirusTotal : Submitted. Polling in background...{RESET}")
        elif vt_resp.status_code == 401:
            print(f"{RED}[!] VirusTotal : Unauthorized.{RESET}")
        else:
            print(f"{RED}[!] VirusTotal : HTTP {vt_resp.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[!] VirusTotal : Submission error — {e}{RESET}")

    # ── VT polling in background thread ───────────────────────────────────────
    vt_result = {'attrs': None, 'done': False}

    def _poll_vt():
        if not vt_submitted:
            vt_result['done'] = True
            return
        MAX_VT = 20
        for _ in range(MAX_VT):
            time.sleep(5)
            try:
                r = requests.get(
                    f'https://www.virustotal.com/api/v3/analyses/{vt_analysis_id}',
                    headers={'x-apikey': get_vt_key()},
                    timeout=15
                )
                if r.status_code == 200:
                    a      = r.json().get('data', {}).get('attributes', {})
                    status = a.get('status', '')
                    total  = sum(a.get('stats', {}).values())
                    if status == 'completed' and total > 0:
                        vt_result['attrs'] = a
                        break
            except Exception:
                break
        vt_result['done'] = True

    vt_thread = threading.Thread(target=_poll_vt, daemon=True)
    vt_thread.start()

    # ── URLscan.io polling in main thread (10s intervals) ─────────────────────
    urlscan_data = None
    urlscan_ok   = False

    if urlscan_submitted and urlscan_uuid:
        MAX_URL     = 12   # up to 2 minutes
        url_attempt = 0
        print(f"\n{YELLOW}[*] Waiting for URLscan.io to finish analysis...{RESET}")

        while url_attempt < MAX_URL:
            time.sleep(10)
            url_attempt += 1
            vt_status_msg = (
                f"{GREEN}VirusTotal report is ready but holding for synchronization.{RESET}"
                if vt_result['done'] and vt_result['attrs']
                else f"{YELLOW}VirusTotal is still scanning.{RESET}"
            )
            try:
                result_resp = requests.get(
                    f'https://urlscan.io/api/v1/result/{urlscan_uuid}/',
                    timeout=15
                )
                if result_resp.status_code == 200:
                    urlscan_data = result_resp.json()
                    urlscan_ok   = True
                    print(f"{GREEN}[+] URLscan.io : Analysis complete.{RESET}")
                    break
                elif result_resp.status_code == 404:
                    print(f"{YELLOW}[*] URLscan is still analyzing... "
                          f"{vt_status_msg} "
                          f"(Attempt {url_attempt}/{MAX_URL}){RESET}")
                else:
                    print(f"{RED}[!] URLscan.io poll: HTTP {result_resp.status_code}{RESET}")
                    break
            except Exception as e:
                print(f"{RED}[!] URLscan.io poll error: {e}{RESET}")
                break

    # Wait for VT thread to finish before displaying anything
    vt_thread.join(timeout=120)

    # ── Display: URLscan first, then VT (shared serial numbering) ─────────────
    SEP = f"{CYAN}  {'─' * 44}{RESET}"
    n   = 1

    if urlscan_ok and urlscan_data:
        page     = urlscan_data.get('page', {})
        verdicts = urlscan_data.get('verdicts', {}).get('overall', {})
        asn_data = urlscan_data.get('meta', {}).get('processors', {}).get('asn', {}).get('data', [])
        isp      = asn_data[0].get('name', 'N/A') if asn_data else 'N/A'

        ip       = page.get('ip',      'N/A')
        country  = page.get('country', 'N/A')
        server   = page.get('server',  'N/A')
        is_mal   = verdicts.get('malicious', False)
        score    = verdicts.get('score', 0)

        v_color  = RED if is_mal else GREEN
        v_label  = 'Malicious' if is_mal else 'Clean'

        print(f"\n{SEP}")
        print(f"  {CYAN}── URLscan.io Report ──{RESET}")
        print(SEP)
        print(f"  {WHITE}{n}. IP Address  : {ip}{RESET}");        n += 1
        print(f"  {WHITE}{n}. Country     : {country}{RESET}");   n += 1
        print(f"  {WHITE}{n}. ISP / ASN   : {isp}{RESET}");       n += 1
        print(f"  {WHITE}{n}. Server      : {server}{RESET}");     n += 1
        print(f"  {v_color}{n}. Verdict     : {v_label} (Score: {score}){RESET}"); n += 1
        print(f"  {GREEN}{n}. Full Report : https://urlscan.io/result/{urlscan_uuid}/{RESET}"); n += 1
    else:
        print(f"\n{RED}[!] URLscan report failed to load.{RESET}")

    # VT engine table — numbering continues from n
    if vt_result['attrs']:
        _display_vt_file_report(
            vt_result['attrs'],
            vt_analysis_id,
            scan_type='url',
            start_n=n
        )
    elif vt_submitted:
        print(f"{YELLOW}[~] VirusTotal: Analysis timed out or returned empty results.{RESET}")
    else:
        print(f"{YELLOW}[~] VirusTotal: Was not submitted.{RESET}")

    input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")

# ─── Module 02 : File Scanner (VirusTotal) ────────────────────────────────────
def scan_file():
    os.system('clear')
    print(BANNER)
    print(f"{GREEN}[::] FILE SCAN MODULE [::]  {RESET}\n")
    print(f"{CYAN}[*] Working directory : {WHITE}{os.getcwd()}{RESET}\n")
    print(f"{GREEN}  upload{RESET}  {WHITE}→ Open file picker (saves as temp_file){RESET}")
    print(f"{GREEN}  scan  {RESET}  {WHITE}→ Submit temp_file to VirusTotal{RESET}")
    print(f"{GREEN}  back  {RESET}  {WHITE}→ Return to main menu{RESET}\n")

    TEMP_FILE = 'temp_file'

    while True:
        cmd = input(f"{GREEN}fire-shield> {RESET}").strip().lower()

        if not cmd:
            continue

        # ── back ───────────────────────────────────────────────────────────────
        if cmd == 'back':
            return

        # ── upload ─────────────────────────────────────────────────────────────
        elif cmd == 'upload':
            print(f"{YELLOW}[*] Opening file picker... Select your file.{RESET}")
            ret = os.system('termux-storage-get temp_file')
            if ret != 0:
                print(f"{RED}[!] File picker failed or was cancelled.{RESET}")
                print(f"{CYAN}[*] Ensure termux-api is installed: pkg install termux-api{RESET}")
            else:
                if os.path.isfile(os.path.join(os.getcwd(), TEMP_FILE)):
                    print(f"{GREEN}[+] File received and saved as 'temp_file'.{RESET}")
                    print(f"{CYAN}[*] Type 'scan' to submit it to VirusTotal.{RESET}")
                else:
                    print(f"{YELLOW}[~] Picker closed but temp_file not found. Did you select a file?{RESET}")

        # ── scan ───────────────────────────────────────────────────────────────
        elif cmd == 'scan':
            filepath = os.path.join(os.getcwd(), TEMP_FILE)
            if not os.path.isfile(filepath):
                print(f"{RED}[!] Error: File not found in current directory.{RESET}")
                print(f"{CYAN}[*] Use 'upload' to pick a file first.{RESET}")
                continue
            break  # File exists — proceed to VT upload below

        # ── unknown command ────────────────────────────────────────────────────
        else:
            print(f"{YELLOW}[!] Unknown command. Valid commands: upload | scan | back{RESET}")

    filepath = os.path.join(os.getcwd(), TEMP_FILE)
    if not os.path.isfile(filepath):
        print(f"\n{RED}[!] Error: File not found in current directory.{RESET}")
        input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")
        return

    print(f"\n{YELLOW}[*] Uploading 'temp_file' to VirusTotal...{RESET}")
    try:
        vt_headers = {'x-apikey': get_vt_key()}
        with open(filepath, 'rb') as f:
            upload_resp = requests.post(
                'https://www.virustotal.com/api/v3/files',
                headers=vt_headers,
                files={'file': (TEMP_FILE, f)},
                timeout=60
            )
        if upload_resp.status_code == 200:
            analysis_id = upload_resp.json().get('data', {}).get('id', '')
            print(f"{YELLOW}[*] File uploaded. Waiting for VirusTotal engines...{RESET}")

            # ── Polling loop: check every 5s until completed ───────────────────
            MAX_ATTEMPTS = 10
            attempt      = 0
            final_attrs  = None

            while attempt < MAX_ATTEMPTS:
                time.sleep(5)
                attempt += 1
                try:
                    poll_resp = requests.get(
                        f'https://www.virustotal.com/api/v3/analyses/{analysis_id}',
                        headers=vt_headers,
                        timeout=15
                    )
                    if poll_resp.status_code == 200:
                        poll_attrs = poll_resp.json().get('data', {}).get('attributes', {})
                        status     = poll_attrs.get('status', '')
                        if status == 'completed':
                            final_attrs = poll_attrs
                            break
                        else:
                            print(f"{YELLOW}[*] Analysis in progress... "
                                  f"Retrying in 5s (Attempt {attempt}/{MAX_ATTEMPTS}){RESET}")
                    else:
                        print(f"{RED}[!] Poll error: HTTP {poll_resp.status_code}{RESET}")
                        break
                except requests.exceptions.ConnectionError:
                    print(f"{RED}[!] Network error during polling.{RESET}")
                    break

            if final_attrs:
                _display_vt_file_report(final_attrs, analysis_id)
            else:
                print(f"{YELLOW}[~] Analysis timed out or incomplete.{RESET}")
                print(f"{CYAN}    Check manually: https://www.virustotal.com/gui/file-analysis/{analysis_id}{RESET}")
        elif upload_resp.status_code == 401:
            print(f"{RED}[!] Unauthorized.{RESET}")
        else:
            print(f"{RED}[!] Upload failed: HTTP {upload_resp.status_code}{RESET}")
    except requests.exceptions.ConnectionError:
        print(f"{RED}[!] Network error during upload.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
    finally:
        # ── Cleanup: delete temp_file regardless of outcome ────────────────────
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
                print(f"\n{CYAN}[*] temp_file deleted from local storage.{RESET}")
            except Exception:
                print(f"\n{YELLOW}[~] Could not delete temp_file. Remove it manually.{RESET}")

    input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")
def scan_ip():
    os.system('clear')
    print(BANNER)
    print(f"{GREEN}[::] IP SCAN MODULE [::]  {RESET}\n")

    ip = input(f"{GREEN}[?] Enter Target IP Address: {RESET}").strip()
    if not ip:
        print(f"\n{RED}[!] No IP entered.{RESET}")
        input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")
        return

    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
        print(f"\n{RED}[!] Invalid IP format. Use IPv4 (e.g. 8.8.8.8){RESET}")
        input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")
        return

    print(f"\n{YELLOW}[*] Querying VirusTotal for IP: {ip}{RESET}")
    try:
        vt_headers = {'x-apikey': get_vt_key()}
        resp = requests.get(
            f'https://www.virustotal.com/api/v3/ip_addresses/{ip}',
            headers=vt_headers,
            timeout=15
        )
        if resp.status_code == 200:
            attrs      = resp.json().get('data', {}).get('attributes', {})
            stats      = attrs.get('last_analysis_stats', {})
            country    = attrs.get('country', 'Unknown')
            owner      = attrs.get('as_owner', 'Unknown')
            reputation = attrs.get('reputation', 0)

            print(f"\n{CYAN}  ── IP Intelligence ──{RESET}")
            print(f"  {WHITE}[i] Country    : {country}{RESET}")
            print(f"  {WHITE}[i] Owner/ASN  : {owner}{RESET}")
            print(f"  {WHITE}[i] Reputation : {reputation}{RESET}")
            _display_vt_stats(stats, label="IP Report")
        elif resp.status_code == 404:
            print(f"{YELLOW}[~] IP not found in VirusTotal database.{RESET}")
        elif resp.status_code == 401:
            print(f"{RED}[!] Unauthorized.{RESET}")
        else:
            print(f"{RED}[!] HTTP {resp.status_code}{RESET}")
    except requests.exceptions.ConnectionError:
        print(f"{RED}[!] Network error.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

    input(f"\n{YELLOW}[*] Press Enter to return to menu...{RESET}")

# ─── Main Loop ────────────────────────────────────────────────────────────────
def main():
    banner()

    while True:
        try:
            choice = show_menu()

            if choice == '01':
                scan_url()
            elif choice == '02':
                scan_file()
            elif choice == '03':
                scan_ip()
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
