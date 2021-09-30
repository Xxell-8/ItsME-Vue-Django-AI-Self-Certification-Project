from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import Serializer

from rest_framework.views import APIView
from .models import Partner, User
from .serializers import ChangePasswordSerializer, PartnerRegisterSerializer, UserSerializer, ProfileSerializer, UserApprovalSerializer, UpdateProfileSerializer, PartnerSerializer, GetUserSerializer

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


@api_view(['POST'])
def get_user(request):
    user = User.objects.filter(code=request.data.get('code'))
    serializer = GetUserSerializer(user, many=True)
    return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK, safe=False)


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 가입 승인 필요한 유저 목록
# 1. auth: 1인지, 회사코드 뭔지 확인 + approval 0인 목록 response
@api_view(['POST'])
def pending(request):
    if request.user.auth:
        pending = User.objects.filter(code=request.user.code, approval=0)
        serializer = GetUserSerializer(pending, many=True)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK, safe=False)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

# 2. code를 주소에 입력해 가져오기
@api_view(['POST'])
def pending_list(request, code):
    pending_list = User.objects.filter(code=code, approval=0)
    serializer = GetUserSerializer(pending_list, many=True)
    if serializer.data:
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK, safe=False)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 해당 회사에 등록된 유저 수
@api_view(['POST'])
def count(request):
    count = User.objects.filter(code=request.user.code)
    if count:
        return JsonResponse({'count': count.count()}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 해당 회사에 등록된 유저 수 2
@api_view(['POST'])
def count_by_code(request, code):
    count = User.objects.filter(code=code)
    if count:
        return JsonResponse({'count': count.count()}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_partner(request, code):
    partner = get_object_or_404(Partner, code=code)
    serializer = PartnerSerializer(partner)
    return Response(serializer.data, status=status.HTTP_200_OK)