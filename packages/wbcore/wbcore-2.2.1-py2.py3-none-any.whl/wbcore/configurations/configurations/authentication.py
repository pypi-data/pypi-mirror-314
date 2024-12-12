from datetime import timedelta

from configurations import values


class Authentication:
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",  # this is default
        "guardian.backends.ObjectPermissionBackend",
    )

    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    JWT_AUTH = {"JWT_AUTH_COOKIE": "JWT"}

    @property
    def SIMPLE_JWT(self):
        return {
            "ACCESS_TOKEN_LIFETIME": timedelta(
                minutes=values.PositiveIntegerValue(5, environ_name="JWT_ACCESS_TOKEN_LIFETIME", environ_prefix=None)
            ),
            "REFRESH_TOKEN_LIFETIME": timedelta(
                days=values.PositiveIntegerValue(1, environ_name="JWT_REFRESH_TOKEN_LIFETIME", environ_prefix=None)
            ),
            "ALGORITHM": "HS256",
            "SIGNING_KEY": self.SECRET_KEY,
            "ROTATE_REFRESH_TOKENS": False,
            "BLACKLIST_AFTER_ROTATION": True,
            "VERIFYING_KEY": None,
            "AUTH_HEADER_TYPES": ("Bearer",),
            "USER_ID_FIELD": "id",
            "USER_ID_CLAIM": "user_id",
            "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
            "TOKEN_TYPE_CLAIM": "token_type",
            "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
            "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
            "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
        }
