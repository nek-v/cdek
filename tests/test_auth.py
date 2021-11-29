# -*- coding: utf-8 -*-

import pytest
from cdek.client.auth import CDEKAuth

def auth():
    return CDEKAuth(
        client_id='EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
        client_secret='PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG',
        prod_environment=False,
    )

def test_var_fetch_token():
    client = auth()
    assert client.connect()