from rest_framework.serializers import ModelSerializer

from posts.models import Post
from users_actions.models import User
from users_actions.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation
