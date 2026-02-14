from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    SelectRoleView,
    CompleteProfileView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("select-role/", SelectRoleView.as_view()),
    path("complete-profile/", CompleteProfileView.as_view()),
]
