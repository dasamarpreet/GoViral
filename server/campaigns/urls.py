from django.urls import path
from .views import (
    CreateCampaignView,
    MyCampaignsView,
    LiveCampaignsView,
    UpdateCampaignStatusView,
    CreatorCampaignSubmissionCreateView,
    CreatorMySubmissionsView,
    CompanySubmissionReviewView
)

urlpatterns = [
    path("create/", CreateCampaignView.as_view()),
    path("my/", MyCampaignsView.as_view()),
    path("live/", LiveCampaignsView.as_view()),
    path("<int:pk>/status/", UpdateCampaignStatusView.as_view()),
    path("submit/", CreatorCampaignSubmissionCreateView.as_view()),
    path("my-submissions/", CreatorMySubmissionsView.as_view()),
    path("submissions/<int:pk>/review/", CompanySubmissionReviewView.as_view())
]
