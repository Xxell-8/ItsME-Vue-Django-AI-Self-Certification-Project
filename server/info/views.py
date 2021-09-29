from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Link, Customer
from .serializers import LinkSerializer, CustomerSerializer
from accounts.models import Partner
import cv2
import numpy as np



# Create your views here.
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def link(request):
    user = request.user

    if request.method == 'GET':
        # 링크 목록 조회
        links = Link.objects.filter(managers__in=[user])
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # 링크 생성
        company = request.data.get('company')
        partner = get_object_or_404(Partner, name=company)
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(partner=partner)
            data = {
                'success': True
            }
            return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def link_detail(request, link_id):
    link = get_object_or_404(Link, pk=link_id)

    if not link.managers.filter(pk=request.user.pk).exists():
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # 링크 상세 조회
        serializer = LinkSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        # 링크 수정
        serializer = LinkSerializer(link, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 링크 삭제
        link.delete()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def customer(request, link_id):
    link = get_object_or_404(Link, pk=link_id)

    if not link.managers.filter(pk=request.user.pk).exists():
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # 해당 링크의 고객정보 확인
        customers = link.customer_set.all()
        serializers = CustomerSerializer(customers, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def id_card_ocr(request):
    # 신분증 OCR 및 비식별화
    image_file = request.FILES['image']
    encoded_img = np.fromstring(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    print(image.shape)
    return Response({})


def compare_info(id_card_info, customer_info):
    # 정보 비교
    for key in customer_info:
        if id_card_info[key] != customer_info[key]:
            return False
    return True


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    link = customer.link
    template = link.template

    if request.method == 'PATCH':
        # 고객 신분증 정보 저장
        if customer.is_completed:
            data = {
                'message': '본인인증이 이미 완료되었습니다.'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {}
            for flag, key in zip([template.id_img, template.id_date, template.id_code], ['img', 'date', 'code']):
                if flag:
                    if request.data.get(key):
                        data[key] = request.data.get(key)
                    else:
                        data = {
                            'message': f'{key}는 필수입력값입니다.'
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)

            serializers = CustomerSerializer(customer, data=data, partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save(is_completed=True)
                return Response(serializers.data, status=status.HTTP_200_OK)
