from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets


class CreateUserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer
    http_method_names = ['post', 'head']
