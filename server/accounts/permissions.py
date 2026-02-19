from rest_framework.permissions import BasePermission


class IsOnboardingComplete(BasePermission):
    """
    Blocks access if:
    - role not selected
    - profile not completed
    """

    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user or not user.is_authenticated:
            return False

        # Role not selected → block
        if not user.role:
            return False

        # Profile not completed → block
        if not user.is_profile_completed:
            return False

        return True


class IsCompany(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "COMPANY"


class IsCreator(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "CREATOR"
