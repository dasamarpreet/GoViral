from django.urls import path
from .views import CompanyDashboardView, CreatorDashboardView

urlpatterns = [
    path("company/", CompanyDashboardView.as_view()),
    path("creator/", CreatorDashboardView.as_view()),
]
