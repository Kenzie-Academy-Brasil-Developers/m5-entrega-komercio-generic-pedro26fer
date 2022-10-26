from rest_framework import mixins
from rest_framework.views import Request
from rest_framework.generics import GenericAPIView


class UpdateCustomAPIView(mixins.UpdateModelMixin,
                          GenericAPIView):

    def patch(self, request:Request, *args, **kwargs):

        keys = request.data.keys()
        list_keys_request = list(keys)

        for key in list_keys_request:
            if key == "is_active" and not request.user.is_superuser:
                del request.data["is_active"]

        return self.partial_update(request, *args, **kwargs)
