from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User



class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(validators=[UniqueValidator(
        queryset=User.objects.all(), message="This usename is not avaible")])

    class Meta:

        model = User

        exclude = ["groups", "user_permissions",
                   "is_staff", "email", "last_login"]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data)

