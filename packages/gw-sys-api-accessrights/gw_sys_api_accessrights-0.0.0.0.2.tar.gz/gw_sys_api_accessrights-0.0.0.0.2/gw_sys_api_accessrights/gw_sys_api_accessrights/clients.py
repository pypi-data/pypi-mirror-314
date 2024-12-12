import typing as _typing
import KeyisBClient

KeyisBAsyncClient = KeyisBClient.AsyncClient()
KeyisBSyncClient = KeyisBClient.Client()


class AsyncClient:
    async def checkRighteByUser(self, token: str, user_id: int, rightName:str) -> _typing.Optional[bool]:
        """
        Возвращает True если у пользователя есть привелегия.

        :return bool: bool
        """
        response = await KeyisBAsyncClient.request('POST', 'mmbps://rights.accounts.gw/checkRighteByUser', json={'token': token, 'user_id': user_id, 'rightName': rightName})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['data']['hasRighte']
            else:
                print(f'Ошибка проверки привелегий: {data["message"]}')
        return None
    
    async def request(self, url: str, json: dict) -> _typing.Optional[dict]:
        response = await KeyisBAsyncClient.request('POST', f'mmbps://rights.accounts.gw/{url}', json=json)
        if response.status_code == 200:
            return response.json()
        else:
            return None

class Client:
    def checkRighteByUser(self, token: str, user_id: int, rightName:str) -> _typing.Optional[bool]:
        """
        Возвращает True если у пользователя есть привелегия.

        :return bool: bool
        """
        response = KeyisBSyncClient.request('POST', 'mmbps://rights.accounts.gw/checkRighteByUser', json={'token': token, 'user_id': user_id, 'rightName': rightName})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['data']['hasRighte']
            else:
                print(f'Ошибка проверки привелегий: {data["message"]}')
        return None
    
    def request(self, url: str, json: dict) -> _typing.Optional[dict]:
        response = KeyisBSyncClient.request('POST', f'mmbps://rights.accounts.gw/{url}', json=json)
        if response.status_code == 200:
            return response.json()
        else:
            return None





