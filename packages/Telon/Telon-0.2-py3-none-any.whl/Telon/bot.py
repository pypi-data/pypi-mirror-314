# pytgbot/bot.py

import requests

class Client:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, chat_id: str, message: str):
        url = f"{self.base_url}sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, data=payload)
        return response.json()

    def send_photo(self, chat_id: str, photo_path: str, caption: str = None):
        url = f"{self.base_url}sendPhoto"
        files = {
            'photo': open(photo_path, 'rb')
        }
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        response = requests.post(url, data=data, files=files)
        files['photo'].close()
        return response.json()

    def send_document(self, chat_id: str, document_path: str, caption: str = None):
        url = f"{self.base_url}sendDocument"
        files = {
            'document': open(document_path, 'rb')
        }
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        response = requests.post(url, data=data, files=files)
        files['document'].close()
        return response.json()

    def get_chat_info(self, chat_id: str):
        url = f"{self.base_url}getChat"
        params = {'chat_id': chat_id}
        response = requests.get(url, params=params)
        return response.json()

    def get_chat_members(self, chat_id: str):
        url = f"{self.base_url}getChatMembersCount"
        params = {'chat_id': chat_id}
        response = requests.get(url, params=params)
        return response.json()

    def kick_member(self, chat_id: str, user_id: int):
        url = f"{self.base_url}kickChatMember"
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }
        response = requests.post(url, data=data)
        return response.json()

    def unban_member(self, chat_id: str, user_id: int):
        url = f"{self.base_url}unbanChatMember"
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }
        response = requests.post(url, data=data)
        return response.json()

    def set_chat_title(self, chat_id: str, title: str):
        url = f"{self.base_url}setChatTitle"
        data = {
            'chat_id': chat_id,
            'title': title
        }
        response = requests.post(url, data=data)
        return response.json()

    def set_chat_description(self, chat_id: str, description: str):
        url = f"{self.base_url}setChatDescription"
        data = {
            'chat_id': chat_id,
            'description': description
        }
        response = requests.post(url, data=data)
        return response.json()

    def get_updates(self):
        url = f"{self.base_url}getUpdates"
        response = requests.get(url)
        return response.json()