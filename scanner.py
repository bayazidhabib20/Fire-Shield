import os
import requests

def fire_shield_scanner():
    print("\n🛡️ --- Fire-Shield Advanced Forensic Tool --- 🛡️")
    print("-" * 50)
    
    target_url = input("Enter target URL to scan: ")
    api_key = input("Enter your URLscan.io API Key: ")
    
    headers = {'API-Key': api_key, 'Content-Type': 'application/json'}
    data = {"url": target_url, "visibility": "unlisted"}
    
    try:
        print("\n[+] Scanning... Please wait.")
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, json=data)
        if response.status_code == 200:
            print(f"\n✅ Scan Successful!")
            print(f"🔗 Result URL: {response.json()['result']}")
        else:
            print(f"\n❌ Error: {response.status_code}")
    except Exception as e:
        print(f"\n⚠️ Connection error: {e}")

if __name__ == "__main__":
    fire_shield_scanner()
