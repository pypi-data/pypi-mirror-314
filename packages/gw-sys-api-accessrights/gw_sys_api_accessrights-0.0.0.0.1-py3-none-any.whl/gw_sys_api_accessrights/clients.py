



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
        response = await KeyisBAsyncClient.request('POST', 'mmbps://accounts.gw/checkRighteByUser', json={'token': token, 'user_id': user_id, 'rightName': rightName})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['data']['hasRighte']
            else:
                print(f'Ошибка проверки привелегий: {data["message"]}')
        return None

class Client:
    def checkRighteByUser(self, token: str, user_id: int, rightName:str) -> _typing.Optional[bool]:
        """
        Возвращает True если у пользователя есть привелегия.

        :return bool: bool
        """
        response = KeyisBSyncClient.request('POST', 'mmbps://accounts.gw/checkRighteByUser', json={'token': token, 'user_id': user_id, 'rightName': rightName})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['data']['hasRighte']
            else:
                print(f'Ошибка проверки привелегий: {data["message"]}')
        return None





