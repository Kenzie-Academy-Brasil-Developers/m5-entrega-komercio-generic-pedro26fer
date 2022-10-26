from rest_framework import mixins
from rest_framework.generics import GenericAPIView


class CustomRetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
