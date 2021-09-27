from django.http import JsonResponse
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from .models import Partner, User
from .serializers import ChangePasswordSerializer, PartnerRegisterSerializer, UserSerializer, ProfileSerializer, UserApprovalSerializer, UpdateProfileSerializer, PartnerSerializer

# 테스트용으로 AllowAny 로 된 부분들 나중에 IsAuthenticated로 변경해야 합니다.

# postman csrftoken error 해결: https://han-py.tistory.com/352

# 파트너 등록: PUT method를 통해 user의 auth를 0에서 1로, 1이면 0으로 바꿔줍니다.
class PartnerRegisterView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PartnerRegisterSerializer


@api_view(['POST'])
def partner_auth(request):
    # 만약 db에 일치하는 코드가 있다면
    if Partner.objects.filter(code=request.data.get('code')):
        # 200 리턴
        return Response(status=status.HTTP_200_OK)
    else:
        # 400 리턴
        return Response({"code": ["일치하는 코드가 없습니다."]}, status=status.HTTP_400_BAD_REQUEST)


class PartnerListAPIView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

# 가입신청 승인: PUT method를 통해 user의 approval을 0에서 1로, 1이면 0으로 바꿔줍니다.
class UserApprovalView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserApprovalSerializer


# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def profile(request, pk):
    user = User.objects.get(pk=pk)
    serializer = ProfileSerializer(user)
    # JsonResponse 한글 깨짐 해결 완료
    return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)


# 참고 URL: https://stackoverflow.com/questions/38845051/how-to-update-user-password-in-django-rest-framework
class ChangePasswordView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateProfileSerializer


@api_view(['POST'])
def delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(status=status.HTTP_200_OK)


def findpwd(request):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

