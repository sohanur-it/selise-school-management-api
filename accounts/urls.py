from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView

router = DefaultRouter()
router.register('register', CreateUserView),

urlpatterns = [
    path('api/v1/', include(router.urls))
]
