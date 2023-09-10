from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['username'] = self.user.username
        data['photo_url'] = self.user.photo_url
        data['icon_id'] = self.user.icon_id
        data['last_login'] = self.user.last_login

        return data
