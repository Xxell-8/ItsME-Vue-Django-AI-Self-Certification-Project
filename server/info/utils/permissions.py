from rest_framework.permissions import BasePermission


class isApproval(BasePermission):
    """
    승인된 유저면 True를 반환,
    승인되지 않은 유져면 False를 반환
    """
    
    def has_permission(self, request, view):
        return bool(request.user.approval)