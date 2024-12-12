from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class UserActivityModelEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbcore:authentication:useractivity-list", args=[], request=self.request)


class UserActivityUserModelEndpointConfig(UserActivityModelEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbcore:authentication:user-useractivity-list", args=[self.view.kwargs["user_id"]], request=self.request
        )


class UserActivityTableEndpointConfig(UserActivityModelEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse("wbcore:authentication:useractivitytable-list", args=[], request=self.request)
