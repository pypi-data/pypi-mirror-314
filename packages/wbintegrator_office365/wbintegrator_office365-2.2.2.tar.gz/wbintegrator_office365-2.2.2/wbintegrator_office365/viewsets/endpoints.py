from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class MixinEndpointConfig(EndpointViewConfig):
    def get_endpoint(self):
        return super().get_endpoint()

    def get_list_endpoint(self):
        return reverse(f"{self.view.get_model().get_endpoint_basename()}-list", request=self.request)

    def get_instance_endpoint(self):
        if self.instance:
            return None
        return super().get_instance_endpoint()

    def get_create_endpoint(self):
        return None

    def get_delete_endpoint(self):
        return None


class TenantUserEndpointConfig(MixinEndpointConfig):
    pass


class EventEndpointConfig(MixinEndpointConfig):
    pass


class CallUserEndpointConfig(MixinEndpointConfig):
    pass


class CallEventEndpointConfig(MixinEndpointConfig):
    pass


class SubscriptionEndpointConfig(MixinEndpointConfig):
    pass


class EventLogEndpointConfig(MixinEndpointConfig):
    pass


class EventLogEventEndpointConfig(MixinEndpointConfig):
    def get_endpoint(self, **kwargs):
        if event_id := self.view.kwargs.get("last_event_id", None):
            return reverse("wbintegrator_office365:event-eventlog-list", args=[event_id], request=self.request)
        return None
