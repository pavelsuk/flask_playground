import json
import requests
import datetime


class ClientAouth(object):
    ''' Client for accessing API from server side
    '''

    def __init__(self,
                 server_url='http://localhost:3010/api/{}',
                 auth_url='https://suk.eu.auth0.com/oauth/token',
                 get_token_body_fname='get_token_body.private',
                 access_token_fname='access_token.private'):
        self._server_url = server_url
        self._auth_url = auth_url
        self._get_token_body_fname = get_token_body_fname
        self._access_token_fname = access_token_fname
        self._access_token = None

    def update_auth_token(self):
        ''' It should mimic the behavior of
        curl -X POST \
            https://suk.eu.auth0.com/oauth/token \
            -H 'Content-Type: application/json' \
            -H 'cache-control: no-cache' \
            -d @get_token_body.private

        and saves the result to file self._access_token_fname
        '''
        print(self._get_token_body_fname)
        with open(self._get_token_body_fname, 'rb') as f:
            get_token_body = json.load(f)
            headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
            r = requests.post(self._auth_url, headers=headers, json=get_token_body)
            resp = r.json()
            print(resp)
            print(resp['access_token'])
            self._access_token = resp['access_token']
            with open(self._access_token_fname, 'w') as access_token_file:
                valid_to = datetime.datetime.now() + datetime.timedelta(seconds=resp['expires_in'])
                print(valid_to)
                resp['valid_to'] = valid_to.strftime('%Y-%m-%d %H:%M:%S')
                json.dump(resp, access_token_file)

    def refresh_auth_token(self):
        ''' Check from the file if the token is supposed to be valid
            and either read the token from the file or update the token
        '''
        valid_to_dt = None
        access_token_json = None

        try:
            with open(self._access_token_fname, 'rb') as access_token_file:
                access_token_json = json.load(access_token_file)
                valid_to = access_token_json['valid_to']
                valid_to_dt = datetime.datetime.strptime(valid_to, '%Y-%m-%d %H:%M:%S')
                if (valid_to_dt > datetime.datetime.now()):
                    self._access_token = access_token_json['access_token']
                else:
                    self.update_auth_token()
        except (FileNotFoundError, KeyError, ValueError):
            self.update_auth_token()

        print('self._access_token = {}'.format(self._access_token))

    def read_data(self):
        ''' reads data via API
            Simulates behavior of
            curl --url 'http://localhost:3010/api/read' --config auth_bearer.private
        '''
        self.refresh_auth_token()

        headers = {
            'Content-Type': 'application/json',
            'cache-control': 'no-cache',
            'Authorization': 'Bearer {}'.format(self._access_token)
        }
        api_endpoint = self._server_url.format('read')
        print('api_endpoint: {}'.format(api_endpoint))
        r = requests.get(api_endpoint, headers=headers)
        resp = r.json()
        print(resp)

    def put_data(self):
        ''' reads data via API
            Simulates behavior of
            curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" --url\
            'http://localhost:3010/api/update' --config auth_bearer.private -X PUT

        '''
        self.refresh_auth_token()

        headers = {
            'Content-Type': 'application/json',
            'cache-control': 'no-cache',
            'Authorization': 'Bearer {}'.format(self._access_token)
        }
        api_endpoint = self._server_url.format('update')
        print('api_endpoint: {}'.format(api_endpoint))
        r = requests.put(api_endpoint, headers=headers, json={"key1": "Hi", "key2": "there"})
        resp = r.json()
        print(resp)


if __name__ == "__main__":
    cl = ClientAouth()
    # cl.refresh_auth_token()
    # cl.read_data()
    cl.put_data()
