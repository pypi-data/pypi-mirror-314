import requests
from requests import Response

class Connection:
    def __init__(self, remote_addr: str):
        self._remote_addr = 'https://' + remote_addr + '/public/'

    def __handle_error(self, response: Response) -> object:
        if response.status_code != 200:
            raise Exception("HTTP Error Code: " + str(response.status_code))
        
        body = response.json()
        if body['retheader']['code'] != 0:
            raise Exception(body['retheader']['msg'])
        
        return body

    def login(self, user: str, password: str):
        self._session = requests.Session()
        response = self._session.post(self._remote_addr + 'login', json = { "user": user, "passwd": password }, verify = False)
        self.__handle_error(response)

    def insert_json_index(self, index: str, item_id: int, object: object):
        state = {
            "index": index,
            "content": [
                { "id": item_id, "value": object }
            ]
         }
        response = self._session.post(self._remote_addr + 'json-index', json = state, verify = False)
        self.__handle_error(response)

    def read_json_index(self, index: str, item_id: int):
        params = { "index": index, "id": item_id }
        response = self._session.get(self._remote_addr + 'json-index', params = params, verify = False)
        body = self.__handle_error(response)
        return body['retdata']
    
    def execute_capsule(self, capsule: str, data: object):
        state = { "name": capsule, "data": data }
        response = self._session.post(self._remote_addr + 'capsule', json = state, verify = False)
        body = self.__handle_error(response)
        return body['retdata']        

    def close(self):
        self._session.close()

