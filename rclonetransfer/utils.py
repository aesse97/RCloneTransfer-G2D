from django.conf import settings
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

def refresh_google_token(user_profile):
    token = user_profile.google_token
    if 'access_token' in token:
        credentials = Credentials.from_authorized_user_info(
            token,
            scopes=settings.GOOGLE_SCOPES,
        )
        if credentials.expired:
            credentials.refresh(Request())

            expiry = credentials.expiry.isoformat() + 'Z' if credentials.expiry else None
            expiry = str(expiry)

            user_profile.google_token = {
                'access_token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
                'expiry': expiry,
            }

        user_profile.save()


def refresh_dropbox_token(user_profile):
    client_id = settings.DROPBOX_CLIENT_ID
    client_secret = settings.DROPBOX_CLIENT_SECRET
    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    def token_saver(token):
        user_profile.dropbox_token = token
        user_profile.save()

    client = BackendApplicationClient(client_id=client_id)
    dropbox = OAuth2Session(client=client, token=user_profile.dropbox_token, auto_refresh_kwargs=extra,
                            auto_refresh_url=settings.DROPBOX_TOKEN_URL, token_updater=token_saver)
    dropbox.get('https://api.dropboxapi.com/2/users/get_current_account')