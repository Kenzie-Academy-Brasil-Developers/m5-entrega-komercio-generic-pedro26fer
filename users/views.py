from rest_framework import generics
from users.models import User
from users.serializer import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from users.permissions import IsAccountOwner
from rest_framework.views import Response, status


class UserView(generics.ListCreateAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer


class UserDetailView(generics.ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    def get_queryset(self):

        max_users = self.kwargs["num"]

        return self.queryset.order_by("-date_joined")[0:max_users]


class UserUpdateView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = User.objects.all()

    serializer_class = UserSerializer

    def partial_update(self, request, *args, **kwargs):

        del request.data["is_active"]
        return super().partial_update(request, *args, **kwargs)


class UserSoftDeleteView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()

    serializer_class = UserSerializer

    def partial_update(self, request, *args, **kwargs):

        request_keys = list(request.data.keys())

        for key in request_keys:
            if key != "is_active":
                del request.data[key]

        return super().partial_update(request, *args, **kwargs)
