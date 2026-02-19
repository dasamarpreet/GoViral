from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOnboardingComplete, IsCompany, IsCreator


class CompanyDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCompany]

    def get(self, request):
        return Response({
            "message": "Welcome to Company Dashboard",
            "email": request.user.email
        })


class CreatorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsOnboardingComplete, IsCreator]

    def get(self, request):
        return Response({
            "message": "Welcome to Creator Dashboard",
            "email": request.user.email
        })
