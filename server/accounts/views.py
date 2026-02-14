from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RoleSelectionSerializer,
    CompanyProfileSerializer,
    CreatorProfileSerializer
)

from django.contrib.auth import get_user_model
from .models import CompanyProfile, CreatorProfile

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoleSelectionSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            request.user.role = serializer.validated_data["role"]
            request.user.save()

            return Response(
                {"message": "Role selected successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Block if profile already completed
        if user.is_profile_completed:
            return Response(
                {"detail": "Profile already completed and cannot be modified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.role == User.Roles.COMPANY:
            serializer = CompanyProfileSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=user)
                user.is_profile_completed = True
                user.save()
                return Response(
                    {"message": "Company profile created"},
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == User.Roles.CREATOR:
            serializer = CreatorProfileSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=user)
                user.is_profile_completed = True
                user.save()
                return Response(
                    {"message": "Creator profile created"},
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(
            {"detail": "Invalid role."},
            status=status.HTTP_400_BAD_REQUEST
        )

