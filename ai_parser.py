import httpx
from read_config import get_openai_api_key

api_key = get_openai_api_key()

def query_gpt_model(size,location,description):
    api_url = 'https://api.openai.com/v1/chat/completions'  # Replace with the correct URL
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer ' + api_key  # Replace with your API key
    }
    data = {
        "model": "gpt-4-1106-preview",
        "messages":[
            {"role": "user", "content": "Extract and clarify the price per square meter (AA), total price in IDR (BB), and detailed location (CC) in bullet points (AA,BB,CC), from the following Indonesian texts:\n\nLuas tanah: " + size + "\nLokasi: " + location + "\nDeskripsi: \"" + description + "\""}
            ],
        "max_tokens": 1000,
        "temperature": 0
    }

    response = httpx.post(api_url, headers=headers, json=data, timeout=30.0)
    response_json = response.json()

    return response_json
