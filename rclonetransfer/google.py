from django.shortcuts import redirect
from django.conf import settings
from requests_oauthlib import OAuth2Session
from django.views import View
from datetime import datetime


class GoogleLoginView(View):
    def get(self, request, *args, **kwargs):
        google = OAuth2Session(settings.GOOGLE_CLIENT_ID,
                               scope=settings.GOOGLE_SCOPES,
                               redirect_uri=settings.GOOGLE_REDIRECT_URI)
        authorization_url, state = google.authorization_url(
            settings.GOOGLE_AUTHORIZATION_BASE_URL,
            access_type='offline',
            prompt='consent'
        )

        request.session['oauth_state'] = state
        return redirect(authorization_url)

class GoogleCallbackView(View):
    def get(self, request, *args, **kwargs):
        google = OAuth2Session(
            settings.GOOGLE_CLIENT_ID,
            state=request.session['oauth_state'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        token = google.fetch_token(
            settings.GOOGLE_TOKEN_URL,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            authorization_response=request.build_absolute_uri(request.get_full_path())
        )

        token['client_id'] = settings.GOOGLE_CLIENT_ID
        token['client_secret'] = settings.GOOGLE_CLIENT_SECRET

        if 'expiry' in token and isinstance(token['expiry'], (int, float)):
            token['expiry'] = datetime.utcfromtimestamp(token['expiry']).isoformat()+'Z'
        elif 'expiry' in token and isinstance(token['expiry'], str):
            if not token['expiry'].endswith('Z'):
                token['expiry'] += 'Z'

        request.user.profile.google_token = token
        request.user.profile.save()

        return redirect('dropboxform')