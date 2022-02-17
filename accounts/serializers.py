from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Organisation, Teacher, Student, ClassSchedule

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
            if user.is_teacher:
                Teacher.objects.create(user=user)
                # teacher = Teacher.objects.create(user=user)
            if user.is_student:
                Student.objects.create(user=user)

        return user


class PublicSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)


martial_choices = (
    ('MARRIED', 'MARRIED'),
    ('UNMARRIED', 'UNMARRIED')
)


class TeacherSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    nid_no = serializers.CharField(required=False)
    martial_status = serializers.ChoiceField(martial_choices)
    birthdate = serializers.DateField(required=False)
    joining_date = serializers.DateField(required=False)

    def create(self, validated_data):
        """Create a new user encrypted password and return it"""
        return Teacher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # teacher = super().update(instance, validated_data)
        # teacher.save()
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        nid_no = validated_data.get('nid_no', instance.nid_no)
        martial_status = validated_data.get('martial_status', instance.martial_status)
        birthdate = validated_data.get('birthdate', instance.birthdate)
        joining_date = validated_data.get('joining_date', instance.joining_date)
        instance.first_name = first_name
        instance.last_name = last_name
        instance.nid_no = nid_no
        instance.martial_status = martial_status
        instance.birthdate = birthdate
        instance.joining_date = joining_date
        instance.save()
        return instance


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = ('__all__')
