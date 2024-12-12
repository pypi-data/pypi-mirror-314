import functools
from datetime import timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import timezone
from jwt import decode as jwt_decode
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import TokenAuthentication as DRFTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from .models import Token

if TYPE_CHECKING:
    from wbcore.contrib.authentication.models import User
else:
    from django.contrib.auth import get_user_model

    User = get_user_model()


class TokenAuthentication(DRFTokenAuthentication):
    """
    Short lived Token token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    model = Token

    # TODO: Find a way to improve typing in the next two methods, somehow pyright is not picking up self.model
    def authenticate_credentials(self, key) -> tuple[User, Token]:
        return super().authenticate_credentials(key)  # type: ignore

    def authenticate(self, request) -> tuple[User, Token] | None:
        authentication_res = super().authenticate(request)
        if authentication_res:
            authentication_res[1].check_validity_for_endpoint(request.resolver_match.view_name, timezone.now())  # type: ignore
        return authentication_res  # type: ignore


class QueryTokenAuthentication(TokenAuthentication):
    """
    Short lived Token token based authentication through query parameters.

    Clients should authenticate by passing the token key "token" as query parameters. For example:
        ?token=401f7ac837da42b97f613d789819ff93537bee6a
    Note, this is unsafe to use this authentication backend on unsecured connection
    """

    query_param_name = "token"

    # TODO: Find a way to improve typing in the next method, somehow pyright is not picking up self.model
    def authenticate(self, request) -> tuple[User, Token] | None:
        token = request.query_params.get(self.query_param_name)
        if not token:
            return None
        user, token = self.authenticate_credentials(token)
        token.check_validity_for_endpoint(request.resolver_match.view_name, timezone.now())
        return user, token  # type: ignore


class JWTCookieAuthentication(BaseAuthentication):
    def authenticate(self, request: "Request") -> tuple[User, UntypedToken] | None:
        jwt_access_token = None
        if cookie_token := request.COOKIES.get("JWT-access", None):
            jwt_access_token = cookie_token
        elif (header_token := request._request.headers.get("Authorization", None)) and (
            len(header_token.split(" ")) == 2
        ):
            jwt_access_token = header_token.split(" ")[1]
        if not jwt_access_token:
            return None
        try:
            token = UntypedToken(jwt_access_token)  # type: ignore -- the 3rd party dependency has a wrong type hint
            decoded_data = jwt_decode(jwt_access_token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=decoded_data["user_id"])
            return (user, token)
        except (
            InvalidToken,
            TokenError,
            KeyError,
            User.DoesNotExist,
            UnboundLocalError,
        ):
            raise AuthenticationFailed("Invalid token")


def inject_short_lived_token(view_name: str | None = None):
    """
    Decorator to wrap around additional resource function which return key value pair of resources and endpoint.
    The decorator will create for the user a short lived token only valid for the requested endpoint and inject it as query parameters

    The decorator expects a view_name (namespace:view_name) to be given otherwise, it will guess it from the resource endpoint (through the resolver)
    Args:
        view_name: Optional, view name to use instead of resolved the endpoint view name
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(serializer, instance, request, user, **kwargs):
            res = {}
            if view_name is None:
                return res
            for key, endpoint in func(serializer, instance, request, user, **kwargs).items():
                res[key] = Token.generate_shareable_link(endpoint, user, protected_view_name=view_name)
            return res

        return wrapper

    return decorator


def unauthenticated(request: "Request") -> dict[str, None]:
    return {"type": None}


def get_user_name(user: User) -> str:
    if method := getattr(user, "get_full_name", None):
        return method()
    return f"{user.first_name} {user.last_name}"


def get_dev_user_from_settings(username_field_key: str) -> list[dict[str, str]]:
    if dev_user := getattr(settings, "DEV_USERS", []):
        users = list()
        for user in dev_user:
            username, password = user.split(":")
            users.append({username_field_key: username, "password": password})
        return users
    return []


def jwt_auth(request: Request) -> dict:
    username_field_key = User.USERNAME_FIELD
    username_field_label = User._meta.get_field(username_field_key).verbose_name

    access = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", timedelta(minutes=5))
    refresh = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME", timedelta(days=1))

    config = {
        "type": "JWT",
        "config": {
            "token": reverse("token_obtain_pair", request=request),
            "refresh": reverse("token_refresh", request=request),
            "verify": reverse("token_verify", request=request),
            "token_lifetime": {"access": access, "refresh": refresh},
            "username_field_key": username_field_key,
            "username_field_label": username_field_label,
        },
    }

    if users := get_dev_user_from_settings(username_field_key):
        config["dev_users"] = users
    return config
