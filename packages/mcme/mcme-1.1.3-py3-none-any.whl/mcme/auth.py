from keycloak import KeycloakOpenID, exceptions
import click

from .logger import log
from .helpers import State

def validate_access_token(keycloak_openid: KeycloakOpenID, keycloak_tokens: dict[str,str]) -> str:
    """Validate the access token on keyloak"""
    if keycloak_tokens:
        token: str = keycloak_tokens["access_token"] if "access_token" in keycloak_tokens else ""
        try:
            keycloak_openid.userinfo(token)
            log.debug("Used saved access token")
            return token
        except exceptions.KeycloakAuthenticationError:
            pass
    return ""

def get_refreshed_tokens(keycloak_openid: KeycloakOpenID, keycloak_tokens: dict[str,str]) -> dict[str,str]:
    """Use refresh token to get a new access token from keycloak"""
    if keycloak_tokens:
        refresh_token: str = keycloak_tokens["refresh_token"] if "refresh_token" in keycloak_tokens else ""
        try:
            refreshed_tokens: dict[str,str] = keycloak_openid.refresh_token(refresh_token)
            log.debug("Used refreshed access token")
            return refreshed_tokens
        except exceptions.KeycloakPostError:
            pass
    return {}

def generate_keycloak_tokens(keycloak_openid: KeycloakOpenID, username: str, password: str) -> dict[str,str]:
    """Get new keycloak access token with username and password"""
    keycloak_tokens: dict[str,str] = keycloak_openid.token(username, password)
    log.debug("Used generated access token")
    return keycloak_tokens

def authenticate(keycloak_openid: KeycloakOpenID, state: State, username: str, password: str) -> str:
    """Get keycloak access token by retrieving saved ones, refreshing it or requesting a new one with username and password"""
    # load state: get current user and saved auth tokens if there are any
    user, tokens = state.get_user_and_tokens(username)
    log.debug("User: " + user) if user is not None else log.debug("No active user")
    # use access token saved in state file if it is valid
    saved_access_token: str = validate_access_token(keycloak_openid, tokens)
    if saved_access_token != "":
        state.update(tokens, user)
        return saved_access_token
    # else: use refresh token saved in state file to refresh access token if it is valid, save to state file
    refreshed_tokens: dict[str,str] = get_refreshed_tokens(keycloak_openid, tokens)
    if refreshed_tokens != {}:
        state.update(refreshed_tokens, user)
        return refreshed_tokens["access_token"]
    # else: generate new access and refresh tokens using username and password, save to state file
    if user is None:
        user = click.prompt('Username', type=str)
    if password is None:
        password = click.prompt('Password', type=str, hide_input=True)
    generated_tokens: dict[str,str] = generate_keycloak_tokens(keycloak_openid, user, password)
    state.update(generated_tokens, user)
    return generated_tokens["access_token"]