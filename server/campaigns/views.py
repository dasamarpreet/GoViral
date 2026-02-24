from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from accounts.permissions import IsCompany, IsOnboardingComplete, IsCreator
from django.utils import timezone
from rest_framework import status
from .models import Campaign, CampaignSubmission
from .serializers import CampaignSerializer, CampaignSubmissionCreateSerializer, CreatorSubmissionStatusSerializer, CompanySubmissionReviewSerializer


# Company ONLY
class CreateCampaignView(APIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCompany]

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)

        if serializer.is_valid():
            deadline = serializer.validated_data.get("deadline_to_bid")

            # Prevent past deadlines
            if deadline and deadline <= timezone.now():
                return Response(
                    {"detail": "Deadline must be in the future."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(company=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Company ONLY
class MyCampaignsView(APIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCompany]

    def get(self, request):
        campaigns = Campaign.objects.filter(
            company=request.user
        ).order_by("-created_at")
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)


# Company ONLY
class UpdateCampaignStatusView(APIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCompany]

    def patch(self, request, pk):
        try:
            campaign = Campaign.objects.get(pk=pk, company=request.user)
        except Campaign.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        status_value = request.data.get("status")

        if status_value not in ["DRAFT", "LIVE", "CLOSED"]:
            return Response({"detail": "Invalid status"}, status=400)

        # Cannot modify closed campaign
        if campaign.status == "CLOSED":
            return Response(
                {"detail": "Closed campaigns cannot be modified."},
                status=400
            )

        # Cannot go LIVE if deadline expired
        if status_value == "LIVE" and campaign.deadline_to_bid <= timezone.now():
            return Response(
                {"detail": "Cannot go live. Bidding deadline already passed."},
                status=400
            )

        campaign.status = status_value
        campaign.save()

        return Response({"message": "Status updated"})


# Creator ONLY
class LiveCampaignsView(APIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCreator]

    def get(self, request):
        campaigns = Campaign.objects.filter(
            status="LIVE",
            deadline_to_bid__gt=timezone.now()
        ).order_by("-created_at")

        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)


# Creator submits content to campaign
class CreatorCampaignSubmissionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCreator]

    serializer_class = CampaignSubmissionCreateSerializer

    def get_queryset(self):
        return CampaignSubmission.objects.filter(
            creator=self.request.user
        )
    

# Creator sees their submission + status
class CreatorMySubmissionsView(ListAPIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCreator]
    serializer_class = CreatorSubmissionStatusSerializer

    def get_queryset(self):
        return CampaignSubmission.objects.filter(
            creator=self.request.user
        ).select_related("campaign", "campaign__company")
    

# Company reviews creator submission 
class CompanySubmissionReviewView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCompany]
    serializer_class = CompanySubmissionReviewSerializer
    queryset = CampaignSubmission.objects.all()

    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.campaign.company != self.request.user:
            raise PermissionError("You are not allowed to review this submission.")
        serializer.save()