from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'is_student', 'is_teacher')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = UserModel.objects.filter(email=validated_data['email'])
        if user:
            raise serializers.ValidationError("The email '" + validated_data['email'] + "' already exists")
        else:
            password = validated_data.pop('password')
            user = UserModel(**validated_data)
            user.set_password(password)
            user.save()

            # create teacher profile
            # if user.is_teacher:
            #     Teacher.objects.create(user=user)
            #     # teacher = Teacher.objects.create(user=user)
            # if user.is_student:
            #     Student.objects.create(user=user)

        return user
