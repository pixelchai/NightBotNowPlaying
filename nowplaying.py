import os
import json
import time
import urllib.parse
import webbrowser
import requests
from typing import Optional


def substitute_string(input_string: str, data: dict):
    output = ""

    buf = ""  # buffer for reading in variable references
    bracket_level = 0
    for char in input_string:
        if char == '{':
            bracket_level += 1
        elif char == '}':
            bracket_level -= 1

            if bracket_level == 0:
                # bracket closed => need to evaluate and flush variable
                output += data.get(buf, "??")
                buf = ""
        else:
            if bracket_level > 0:  # if within a bracket
                buf += char
            else:
                output += char

    if bracket_level > 0:
        print("Warning: your string has {} unclosed bracket(s)!".format(bracket_level))
    elif bracket_level < 0:
        print("Warning: your string has {} unopened bracket(s)!".format(-bracket_level))
    return output


class Client:
    URI_AUTH = "https://api.nightbot.tv/oauth2/authorize"
    URI_TOKEN = "https://api.nightbot.tv/oauth2/token"
    URI_API = "https://api.nightbot.tv/1/"
    URI_REDIRECT = "https://localhost:5771"

    def __init__(self):
        self.auth_path = os.environ.get("AUTH_PATH", "auth.json")
        self.session = requests.Session()

        # get access token
        access_token = self._get_token()
        if access_token is None:
            return

        self.session.headers.update({'Authorization': 'Bearer {0}'.format(access_token)})

    def _authorize(self, auth_data):
        try:
            params = {
                'client_id': auth_data['client_id'],
                'client_secret': auth_data['client_secret'],
                'scope': 'song_requests_queue',
                'redirect_uri': Client.URI_REDIRECT,
                'response_type': 'code'
            }
        except KeyError:
            print("Your auth.json file either is corrupted or does not exist.")
            return None

        webbrowser.open(Client.URI_AUTH + "?" + urllib.parse.urlencode(params))

        code = input("Please enter the code: ").strip()
        return self._request_access_token(code, auth_data)

    def _request_access_token(self, code, auth_data) -> Optional[str]:
        time_requested = time.time()
        data = {
            'client_id': auth_data['client_id'],
            'client_secret': auth_data['client_secret'],
            'grant_type': 'authorization_code',
            'redirect_uri': Client.URI_REDIRECT,
            'code': code
        }
        try:
            response = self.session.post(Client.URI_TOKEN, data=data)
            if response.status_code == 200:
                token_data = json.loads(response.text)

                # save access token
                try:
                    auth_data.update({
                        'access_token': token_data['access_token'],
                        'refresh_token': token_data['refresh_token'],
                        'expire_timestamp': time_requested + token_data['expires_in']
                    })
                    assert token_data['token_type'] == 'bearer'

                    # write data to file
                    with open(self.auth_path, "w") as f:
                        json.dump(auth_data, f)

                    # return access_token
                    return auth_data.get('access_token', None)
                except (KeyError, AssertionError):
                    print("The access token received was not as expected")
            else:
                print("Error getting access token:")
                print(response.text)
        except requests.HTTPError:
            print("An HTTPError occurred while requesting an access token")

        return None

    def _get_token(self) -> Optional[str]:
        # load auth data from auth.json if it exits
        auth_data = {}
        if os.path.isfile(self.auth_path):
            with open(self.auth_path, "r") as f:
                auth_data = json.load(f)

        if 'access_token' not in auth_data:
            # access token does not exist, so must authorize
            return self._authorize(auth_data)
        else:  # access token exists
            try:
                expire_timestamp = auth_data['expire_timestamp']
                if time.time() > expire_timestamp:
                    # maybe implement the actual refresh protocol here.
                    # for now, just reauthorize instead (which should also work fine)
                    print("Auth expired! Need to reauthorize...")
                    return self._authorize(auth_data)
                else:
                    # not expired
                    return auth_data['access_token']
            except KeyError:
                print("Your auth.json file is likely corrupted.")
                return None

    def get_queue(self):
        try:
            response = self.session.get("{}song_requests/queue".format(Client.URI_API))
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print("Error getting song queue:")
                print(response.text)
        except (requests.HTTPError, requests.exceptions.SSLError) as ex:
            print('An exception occurred while getting the song queue.', ex)
