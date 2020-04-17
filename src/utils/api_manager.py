import requests
import yaml


class APIManager:
    base_url = 'https://epimodo.gastbob40.ovh/api/'

    def get_data(self, type: str, **filters):
        headers = self.get_headers()
        url = self.base_url + type + '/?'

        for key, value in filters.items():
            url += f'{key}={value}&'

        r = requests.get(url, headers=headers)

        if not r.ok:
            return False, f'API error: {r.reason}'
        else:
            return True, r.json()

    def post_data(self, type, **body):
        headers = self.get_headers()

        r = requests.post(self.base_url + type + '/', json=body, headers=headers)

        if not r.ok:
            return False, r.reason
        else:
            return True, r.json()

    def edit_data(self, type, id, **body):
        headers = self.get_headers()

        r = requests.put(self.base_url + type + '/' + str(id) + '/', json=body, headers=headers)

        if not r.ok:
            return False, r.reason
        else:
            return True, r.json()

    @staticmethod
    def get_headers():
        with open('run/config/tokens.yml', 'r') as file:
            token = yaml.safe_load(file)['epimodo_website_token']

        return {
            'content-type': 'application/json',
            'Authorization': f'Token {token}'
        }
