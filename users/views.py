from rest_framework import generics
from users.models import User
from users.serializer import UserSerializer


class UserView(generics.ListCreateAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer


class UserDetailView(generics.ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    def get_queryset(self):

        max_users = self.kwargs["num"]

        return self.queryset.order_by("-date_joined")[0:max_users]
