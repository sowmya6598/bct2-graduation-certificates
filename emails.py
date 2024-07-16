import os
import base64
import requests

folder_path = r"your_folder_path"
mandrill_api_key = 'API_KEY'

subject = 'subject line'
body = "body of email"

sender_email = 'email'
sender_name = 'name'

def send_email(receiver_email, subject, body, image_path):
    with open(image_path, 'rb') as img:
        data = img.read()
        encoded_image = base64.b64encode(data).decode()

    message = {
        "key": mandrill_api_key,
        "message": {
            "from_email": sender_email,
            "from_name": sender_name,
            "to": [{"email": receiver_email}],
            "subject": subject,
            "html": body,
            "attachments": [
                {
                    "type": "image/png",
                    "name": os.path.basename(image_path),
                    "content": encoded_image
                }
            ]
        }
    }

    try:
        response = requests.post(
            'https://mandrillapp.com/api/1.0/messages/send.json',
            json=message
        )
        response_data = response.json()
        if response.status_code == 200:
            print(f'Email sent to {receiver_email}')
        else:
            print(f'Failed to send email to {receiver_email}: {response_data}')
    except Exception as e:
        print(f'Failed to send email to {receiver_email}: {e}')

for filename in os.listdir(folder_path):
    email_address = os.path.splitext(filename)[0]
    image_path = os.path.join(folder_path, filename)
    send_email(email_address, subject, body, image_path)