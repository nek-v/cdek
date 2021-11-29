# -*- coding: utf-8 -*-

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class CDEKAuth():

    def __init__(self, client_id, client_secret, prod_environment):
        self.client_secret = client_secret
        self.client_id = client_id
        if not prod_environment:
            self.url = 'https://api.edu.cdek.ru/v2/oauth/token?grant_type=client_credentials'
        else:
            self.url = 'https://api.cdek.ru/v2/oauth/token?grant_type=client_credentials'

    def connect(self):
        oauth_client = BackendApplicationClient(client_id=self.client_id)
        oauth_session = OAuth2Session(client=oauth_client)
        token = oauth_session.fetch_token(token_url=self.url,
                                          client_id=self.client_id,
                                          client_secret=self.client_secret)
        return OAuth2Session(client_id=self.client_id, token=token)
