from urllib.parse import quote
import requests


def send_message(chat_id, message_to_send, telegram_token):
    print(message_to_send)
    encoded_message = quote(message_to_send)
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={encoded_message}"
    result = requests.get(url).json()
    print("answer is: " + str(result))
    return result