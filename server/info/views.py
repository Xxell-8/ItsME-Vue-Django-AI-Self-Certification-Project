from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Link
from .serializers import LinkListSerializer, CustomerSerializer, LinkDetailSerializer, IdCardSerializer
from accounts.models import Partner
import cv2
import numpy as np
from django.utils import timezone
from .utils.ocr import ocr
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile



# Create your views here.
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def link(request):
    user = request.user

    if request.method == 'GET':
        # 링크 목록 조회
        links = Link.objects.filter(managers__in=[user], expired_at__gt=timezone.now())
        serializer = LinkListSerializer(links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # 링크 생성
        company = request.data.get('company')
        partner = get_object_or_404(Partner, name=company)
        serializer = LinkDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(partner=partner)
            data = {
                'success': True
            }
            return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def link_detail(request, link_path):
    link = get_object_or_404(Link, path=link_path)

    if not link.managers.filter(pk=request.user.pk).exists():
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # 링크 상세 조회
        if link.expired_at <= timezone.now():
            data = {
                'message': '만료된 링크입니다.'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        serializer = LinkDetailSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 링크 삭제
        link.delete()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def id_card_ocr(request, link_path):
    # 신분증 OCR 및 비식별화
    image_file = request.FILES.get('img')
    encoded_img = np.fromstring(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    result = ocr(image)
    img = result.get('img')
    cv2.imwrite(f'./media/{link_path}/{image_file.name}', img)
    result = {
        'birth': '940212',
        'name': '홍길동',
        'img': f'{link_path}/{image_file.name}'
    }
    serializer = IdCardSerializer(data=result)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def customer(request, link_path):
    name = request.data.get('name')
    if not name:
        data = {'message': '이름은 필수값입니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    birth = request.data.get('birth')
    if not birth:
        data = {'message': '생일은 필수값입니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    link = get_object_or_404(Link, path=link_path)
    customers = link.customers.filter(name=name, birth__endswith=birth)
    if not customers.exists():
        # 정보가 일치하는 사람이 없을 때
        data = {
            'message': '정보가 일치하지 않습니다.'
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    customers = customers.filter(is_completed=False)
    if not customers.exists():
        # 이미 인증이 완료되었을 때
        data = {
            'message': '이미 인증이 완료되었습니다.'
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    # 정보가 일치하는 사람이 있으면 마스킹된 신분증 이미지를 저장
    customer = customers[0]
    data = {
        'is_completed': True,
        'img': request.data.get('img')
    }
    serializer = CustomerSerializer(customer, data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_200_OK)