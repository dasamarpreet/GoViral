from django.urls import path
from .views import (
    CreateCampaignView,
    MyCampaignsView,
    LiveCampaignsView,
    UpdateCampaignStatusView,
)

urlpatterns = [
    path("create/", CreateCampaignView.as_view()),
    path("my/", MyCampaignsView.as_view()),
    path("live/", LiveCampaignsView.as_view()),
    path("<int:pk>/status/", UpdateCampaignStatusView.as_view()),
]
