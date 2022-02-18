from rest_framework import serializers
from .models import Teacher, ClassSchedule, Organisation


class PublicSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)

    def create(self, validated_data):
        """Create a new organisation and return it"""
        return Organisation.objects.create(**validated_data)


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


class ClassSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    class_name = serializers.CharField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    teacher = TeacherSerializer(read_only=True)

    def create(self, validated_data):
        """Create a new class schedule encrypted password and return it"""
        return ClassSchedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a class schedule, setting the password correctly and return it"""
        # teacher = super().update(instance, validated_data)
        # teacher.save()
        class_name = validated_data.get('class_name', instance.class_name)
        start_time = validated_data.get('start_time', instance.start_time)
        end_time = validated_data.get('end_time', instance.end_time)
        instance.class_name = class_name
        instance.start_time = start_time
        instance.end_time = end_time
        instance.save()
        return instance
