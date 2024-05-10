import requests
import threading
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv("TELEGRM_TOKEN")
telegram_chat_id = os.getenv("CHAT_ID")

# Server's address
server_address = 'https://app.slack.com/client/T032XS1SL0M/D06S9D3B3PU'

last_status = None

def send_telegram_message(message):

    sendData = {
        "chat_id" : telegram_chat_id,
        "text" : message,
    }

    telegramURL = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    response = requests.post(telegramURL, sendData)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Error sending message: {}".format(response.status_code))

def check_server():
    global last_status
    try:
        response = requests.get(server_address, timeout = 30)
        print('Send get request')
        status = response.status_code
    except requests.exceptions.RequestException as e:
        status = str(e)

    if status != last_status:
        if isinstance(status, int) and status == 200:
            send_telegram_message(f'Server is up: {status}')
        else:
            send_telegram_message(f'Server issue detected: {status}')
        last_status = status

def main():
    while True:
        threading.Thread(target=check_server).start()
        sleep(1)

if __name__ == '__main__':
    main()