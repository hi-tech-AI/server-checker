import requests
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv("TELEGRM_TOKEN")
telegram_chat_id = os.getenv("CHAT_ID")

# Server's address
server_address = 'https://app.slack.com/client/T032XS1SL0M/D06S9D3B3PU'

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
    try:
        response = requests.get(server_address, timeout = 30)
        if response.status_code == 200:
            return 'Server is started'
        else:
            return 'Server is not responding normally'
    except requests.exceptions.RequestException as e:
        return 'Server is stopped'

def main():
    last_status = None
    while True:
        current_status = check_server()
        if current_status != last_status:
            send_telegram_message(message = current_status)
            last_status = current_status
        else:
            print('None change server')
        sleep(1)

if __name__ == '__main__':
    main()