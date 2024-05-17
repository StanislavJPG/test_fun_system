from rest_framework.serializers import ModelSerializer

from users_actions.models import User, Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'username', 'email', 'date_joined',
                  'name', 'phone', 'website', 'address')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        address = AddressSerializer(instance.address)
        representation['address'] = address.data
        return representation
