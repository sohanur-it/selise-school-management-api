from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Organisation, Teacher,ClassSchedule
from .serializers import PublicSerializer, TeacherSerializer, ClassSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination


class PublicApiView(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = PublicSerializer


class OrganisationList(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicSerializer

    def get(self, request, format=None):
        organisation = Organisation.objects.all()
        serializer = PublicSerializer(organisation, many=True)
        return Response({
            "data": serializer.data,
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)


class OrganisationDetails(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, id, format=None):
        organisations = Organisation.objects.get(id=id)
        serializer = PublicSerializer(organisations)

        return Response({
            "data": serializer.data,
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)


class TeacherList(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeacherSerializer

    def get(self, request, format=None):
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response({
            "data": serializer.data,
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        if serializer.is_valid():
            workspace = serializer.save(user=request.user)
            return Response({
                "data": serializer.data,
                "response_code": status.HTTP_201_CREATED,
                "response_message": "created"
            })
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": serializer.errors
            })


class TeacherDetails(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeacherSerializer

    def get(self, request, id, format=None):
        if request.user.is_admin or request.user.is_teacher:
            teacher = Teacher.objects.get(id=id)
            serializer = TeacherSerializer(teacher)

            return Response({
                "data": serializer.data,
                "response_code": status.HTTP_200_OK,
                "response_message": "success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "response_message": 'UNATHORIZED'

            })

    def put(self, request, id, format=None):
        if request.user.is_admin:
            teacher = Teacher.objects.get(id=id)
            serializer = TeacherSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "data": serializer.data,
                    "response_code": status.HTTP_200_OK,
                    "response_message": "success"
                }, status=status.HTTP_200_OK)
            return Response({
                "data": {},
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "response_message": 'UNATHORIZED'

            })


class ClassList(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassSerializer

    def get(self, request, format=None):
        class_list = ClassSchedule.objects.all()
        serializer = self.get_serializer(class_list, many=True)
        return Response({
            "data": serializer.data,
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        if serializer.is_valid():
            class_obj = serializer.save(teacher=request.user.teacher)
            return Response({
                "data": serializer.data,
                "response_code": status.HTTP_201_CREATED,
                "response_message": "created"
            })
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": serializer.errors
            })


class ClassDeatils(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassSerializer

    def get(self, request, id, format=None):
        if request.user.is_student:
            teacher = ClassSchedule.objects.get(id=id)
            serializer = self.get_serializer(teacher)

            return Response({
                "data": serializer.data,
                "response_code": status.HTTP_200_OK,
                "response_message": "success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "response_message": 'UNATHORIZED'

            })

    def put(self, request, id, format=None):
        if request.user.is_teacher:
            class_obj = ClassSchedule.objects.get(id=id)
            serializer = self.get_serializer(class_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "data": serializer.data,
                    "response_code": status.HTTP_200_OK,
                    "response_message": "success"
                }, status=status.HTTP_200_OK)
            return Response({
                "data": {},
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "response_message": 'UNATHORIZED'

            })


class CreateUserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer
    http_method_names = ['post', 'head']
