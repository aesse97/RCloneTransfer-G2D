from django.shortcuts import redirect
from django.conf import settings
from requests_oauthlib import OAuth2Session
from django.views import View

class DropboxLoginView(View):
    def get(self, request, *args, **kwargs):
        dropbox = OAuth2Session(settings.DROPBOX_CLIENT_ID,
                                scope=settings.DROPBOX_SCOPES,
                                redirect_uri=settings.DROPBOX_REDIRECT_URI)
        authorization_url, state = dropbox.authorization_url(
            settings.DROPBOX_AUTHORIZATION_BASE_URL,
            token_access_type='offline'
        )

        request.session['oauth_state'] = state
        return redirect(authorization_url)


class DropboxCallbackView(View):
    def get(self, request, *args, **kwargs):
        dropbox = OAuth2Session(
            settings.DROPBOX_CLIENT_ID,
            state=request.session['oauth_state'],
            redirect_uri=settings.DROPBOX_REDIRECT_URI
        )
        token = dropbox.fetch_token(
            settings.DROPBOX_TOKEN_URL,
            client_secret=settings.DROPBOX_CLIENT_SECRET,
            authorization_response=request.build_absolute_uri(request.get_full_path())
        )

        token['client_id'] = settings.DROPBOX_CLIENT_ID
        token['client_secret'] = settings.DROPBOX_CLIENT_SECRET

        request.user.profile.dropbox_token = token
        request.user.profile.save()

        return redirect('rclonebutton')