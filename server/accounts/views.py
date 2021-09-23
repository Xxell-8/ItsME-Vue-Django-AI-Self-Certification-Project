from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Partner, User
from .serializers import PartnerSerializer, UserSerializer, UserLoginSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def partner(request):
    serializer = PartnerSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        partner = serializer.save()
        partner.set_password(request.data.get('password'))
        partner.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def partner_auth(request):
    # 만약 db에 일치하는 코드가 있다면
    if Partner.objects.filter(code=request.data.get('code')):
        # 200 리턴
        return Response(status=status.HTTP_200_OK)
    else:
        # 400 리턴
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approval(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 만약 사용자의 approval 이 1이면 0으로(승인 취소), 0이면 1로(승인)
        if user.approval:
            user.approval = 0
        else:
            user.approval = 1
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def join(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request body error.'}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['username'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)

        response = {
            'success': 'True',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)


def profile(request):
    pass


def changepwd(request):
    pass


def findpwd(request):
    pass
