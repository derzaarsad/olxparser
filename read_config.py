import json
import os

# Path to your JSON configuration file
config_file_path = 'config.json'

# Check if the configuration file exists
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"The configuration file '{config_file_path}' does not exist.")

def get_chat_id_list():
    try:
        # Reading the JSON file
        with open(config_file_path, 'r') as file:
            config = json.load(file)

        # Check if 'chat_id' field exists in the JSON data
        if 'chat_id' not in config:
            raise ValueError("The 'chat_id' field is missing in the configuration file.")

        # Accessing the list of IDs
        chat_id = config['chat_id']

        # Ensure that 'chat_id' is a list
        if not isinstance(chat_id, list):
            raise TypeError("The 'chat_id' field should be a list.")

        # Do something with the chat_id
        return chat_id
    except json.JSONDecodeError:
        raise ValueError(f"The file '{config_file_path}' does not contain valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_openai_api_key():
    try:
        # Reading the JSON file
        with open(config_file_path, 'r') as file:
            config = json.load(file)

        # Check if 'openai_api_key' field exists in the JSON data
        if 'openai_api_key' not in config:
            raise ValueError("The 'openai_api_key' field is missing in the configuration file.")

        # Accessing the list of IDs
        openai_api_key = config['openai_api_key']

        # Ensure that 'openai_api_key' is a list
        if not isinstance(openai_api_key, str):
            raise TypeError("The 'openai_api_key' field should be a list.")

        # Do something with the openai_api_key
        return openai_api_key
    except json.JSONDecodeError:
        raise ValueError(f"The file '{config_file_path}' does not contain valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_telegram_api_key():
    try:
        # Reading the JSON file
        with open(config_file_path, 'r') as file:
            config = json.load(file)

        # Check if 'telegram_api_key' field exists in the JSON data
        if 'telegram_api_key' not in config:
            raise ValueError("The 'telegram_api_key' field is missing in the configuration file.")

        # Accessing the list of IDs
        telegram_api_key = config['telegram_api_key']

        # Ensure that 'telegram_api_key' is a list
        if not isinstance(telegram_api_key, str):
            raise TypeError("The 'telegram_api_key' field should be a list.")

        # Do something with the telegram_api_key
        return telegram_api_key
    except json.JSONDecodeError:
        raise ValueError(f"The file '{config_file_path}' does not contain valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
