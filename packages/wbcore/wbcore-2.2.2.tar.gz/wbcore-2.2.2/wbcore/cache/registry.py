import typing
from contextlib import suppress
from dataclasses import dataclass
from typing import Callable, Generator

from django.core.cache import cache
from dynamic_preferences.models import global_preferences_registry
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate
from wbcore.contrib.authentication.models import User
from wbcore.filters.defaults import RequiredFilterMissing

if typing.TYPE_CHECKING:
    from wbcore.pandas.views import PandasAPIViewSet
    from wbcore.viewsets import ChartViewSet


@dataclass
class CachedClass:
    view_class: type["PandasAPIViewSet"] | type["ChartViewSet"]
    view_kwargs: list[dict[str, str]] | Callable | None = None
    get_parameters: list[dict[str, str]] | Callable | None = None

    def _get_requests(self) -> Generator[Request, None, None]:
        """
        Given the stored list of GET parameters, returns a list of instantiated request with the system user as request.user

        Returns:
            A generator of DRF Request
        """
        system_user_email = global_preferences_registry.manager()["wbcore__system_user_email"]
        get_parameters = self.get_parameters if self.get_parameters else [{}]
        if callable(self.get_parameters):
            get_parameters = get_parameters()

        for get_parameter in get_parameters:
            request = APIRequestFactory().get("", data=get_parameter)
            user = User.objects.get(email=system_user_email)
            force_authenticate(request, user=user)
            request.user = user
            yield Request(request)

    def fetch_cache(self) -> typing.Any:
        """
        For every kwargs and requests, reset the cache and get the view dataframe. This hits under the hood the caching mechanism

        Returns:
            A list of generated dataframe
        """
        view_kwargs = self.view_kwargs if self.view_kwargs else [{}]
        if callable(self.view_kwargs):
            view_kwargs = view_kwargs()
        res = []
        for request in self._get_requests():
            for kwargs in view_kwargs:
                with suppress(RequiredFilterMissing):
                    view = self.view_class(request=request, kwargs=kwargs)
                    setattr(request, "parser_context", {"request": request, "view": view, "kwargs": kwargs})
                    cache_key = view._get_cache_key()
                    cache.delete(cache_key)
                    res.append(view._get_dataframe())
        return res


class PeriodicCacheRegistry:
    """
    Registry to hold the api view classes that needs to recompute their cache periodically
    """

    classes = list[CachedClass]

    def __init__(self):
        self.classes = []

    def add(
        self,
        view_class: type["PandasAPIViewSet"] | type["ChartViewSet"],
        view_kwargs: list[dict[str, str]] | Callable | None = None,
        get_parameters: list[dict[str, str]] | Callable | None = None,
    ):
        self.classes.append(
            CachedClass(
                view_class=view_class,
                view_kwargs=view_kwargs,
                get_parameters=get_parameters,
            )
        )


periodic_cache_registry = PeriodicCacheRegistry()
