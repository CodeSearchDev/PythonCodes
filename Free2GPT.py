import time
import requests
import json
from hashlib import sha256

API_URL = "https://chat10.free2gpt.xyz/api/generate"

def generate_response(message):
    timestamp = int(time.time() * 1e3)
    sign = sha256(f"{timestamp}:{message}:".encode()).hexdigest()
    
    data = {"messages": [{"role": "user", "content": message}], "time": timestamp, "pass": None, "sign": sign}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code != 200:
            return response.text

        try:
            json_response = response.json()
            return json_response.get("choices", [{}])[0].get("message", response.text)
        except json.JSONDecodeError:
            return response.text

    except requests.RequestException as e:
        return str(e)

if __name__ == "__main__":
    response = generate_response("Hey, how are you?")
    print(response)