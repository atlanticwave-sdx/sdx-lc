from typing import List

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

from connexion.exceptions import OAuthProblem

TOKEN_DB = {"asdf1234567890": {"uid": 100}}

# def check_api_key(api_key, required_scopes):
#    return {'test_key': 'test_value'}


def check_api_key(api_key, required_scopes):
    info = TOKEN_DB.get(api_key, None)

    if not info:
        raise OAuthProblem("Invalid api_key")

    return info


def get_secret(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


def check_topology_auth(token):
    return {"scopes": ["read:topology", "write:topology"], "uid": "test_value"}


def validate_scope_topology_auth(required_scopes, token_scopes):
    return set(required_scopes).issubset(set(token_scopes))
