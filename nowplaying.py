import os
import json
import time
from typing import Optional

from NightPy.nightpy import NightPy

class Client:
    def __init__(self, scope="song_requests song_requests_queue"):
        # get auth token
        auth_token = self.get_token()
        if auth_token is None:
            return

        self.np = NightPy(auth_token)

    def _authorize(self, auth_data):
        pass

    def _refresh(self, auth_data):
        pass  # todo

    def get_token(self) -> Optional[str]:
        # load auth data from auth.json if it exits
        auth_data = {}
        if os.path.isfile("auth.json"):
            with open("auth.json", "r") as f:
                auth_data = json.load(f)

        if 'access_token' not in auth_data:
            # access token does not exist, so must authorize
            self._authorize(auth_data)
        else:  # access token exists
            try:
                expire_timestamp = auth_data['expire_timestamp']
                if time.time() > expire_timestamp:
                    # maybe implement the actual refresh protocol here.
                    # for now, just reauthorize instead (which should also work fine)
                    print("Auth expired! Need to reauthorize...")
                    self._authorize(auth_data)
                else:
                    # not expired
                    return auth_data['access_token']
            except KeyError:
                print("Your auth.json file is likely corrupted.")
                return None
