from langchain_core.exceptions import LangChainException

APIStatusErrors = [LangChainException]

try:
    from openai._exceptions import (
        AuthenticationError,
        BadRequestError,
        ConflictError,
        InternalServerError,
        NotFoundError,
        PermissionDeniedError,
        RateLimitError,
        UnprocessableEntityError,
    )

    APIStatusErrors.extend(
        [
            BadRequestError,
            AuthenticationError,
            PermissionDeniedError,
            NotFoundError,
            ConflictError,
            UnprocessableEntityError,
            RateLimitError,
            InternalServerError,
        ]
    )
except ImportError:
    pass


try:
    from anthropic._exceptions import (
        APIConnectionError,
        APIResponseValidationError,
        APIStatusError,
    )

    APIStatusErrors.extend([APIResponseValidationError, APIStatusError, APIConnectionError])
except ImportError:
    pass
