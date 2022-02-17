from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, OrganisationList, OrganisationDetails, TeacherList, TeacherDetails, ClassList, \
    ClassDeatils

router = DefaultRouter()
router.register('register', CreateUserView),

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/organisations', OrganisationList.as_view()),
    path('api/v1/organisations/<int:id>', OrganisationDetails.as_view()),
    path('api/v1/teachers', TeacherList.as_view()),
    path('api/v1/teachers/<int:id>', TeacherDetails.as_view()),
    path('api/v1/class', ClassList.as_view()),
    path('api/v1/class/<int:id>', ClassDeatils.as_view())
]
