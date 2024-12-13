import json
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import AllowAllUsersModelBackend, ModelBackend
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.core.validators import validate_email
from django.conf import settings
from jwkest import BadSyntax
from jwkest.jwt import JWT
from jwt.utils import base64url_decode, base64url_encode
from oidc_provider.lib.utils.dpop import (
    verify_signature,
    verify_dpop_proof,
    verify_thumbprint,
)
from oidc_provider.models import Token
from oidc_provider.views import JwksView
import inspect
from oidc_provider.models import Client

from djangoldp_account.auth.solid import Solid
from djangoldp_account.errors import LDPLoginError

UserModel = get_user_model()


class BasicAuthBackend(AllowAllUsersModelBackend):
    def validate_bearer_token(self, token):
        try:
            token = Token.objects.get(access_token=token)
            if token:
                client_email = token.client.contact_email
                user = UserModel.objects.filter(email=client_email).first()

                if self.user_can_authenticate(user):
                    return user
        except Exception as e:
            raise e

        return None

    def authenticate(self, request, *args, **kwargs):
        if "HTTP_AUTHORIZATION" in request.META:
            jwt = request.META["HTTP_AUTHORIZATION"]

            if jwt.lower().startswith("bearer"):
                jwt = jwt[7:]

                # make an attempt assuming Bearer token if not recognised or not specified
                return self.validate_bearer_token(jwt)

        return ModelBackend().authenticate(request, *args, **kwargs)
