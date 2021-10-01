from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import IdCard, Link
from .serializers import LinkListSerializer, CustomerSerializer, LinkDetailSerializer, IdCardSerializer
from accounts.models import Partner
import cv2
from django.utils import timezone
from .utils.ocr import ocr
from .utils.image import base64_to_image, get_random_string
from django.core.files.base import ContentFile
from PIL import Image




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
    link = get_object_or_404(Link, path=link_path)
    # 신분증 OCR 및 비식별화
    image_base64 = request.data.get('id_card_image')
    image = base64_to_image(image_base64)
    result = ocr(image)
    if not result:
        data = {
            'message': '신분증 OCR에 실패했습니다.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    img = result.get('img')
    image_io = cv2.imencode('.jpg', img)[1].tostring()
    image_file = ContentFile(image_io, name=f'{link_path}/{get_random_string()}.jpg')
    result['img'] = image_file

    # 얼굴 유사도 검사
    face = request.data.get('face')
    id_card_face = request.data.get('id_card_face')
    result['face_similarity'] = True
    
    serializer = IdCardSerializer(data=result)
    if serializer.is_valid(raise_exception=True):
        serializer.save(link=link)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    id_card = get_object_or_404(IdCard, pk=request.data.get('id_card'))
    data = {
        'is_completed': id_card.face_similarity,
        'img': id_card.img
    }
    serializer = CustomerSerializer(customer, data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        data = {
            'success': True
        }
        id_card.delete()
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def link_count(request, partner_id):
    partner = get_object_or_404(Partner, pk=partner_id)
    link_count = partner.links.count()
    data = {
        'link_count': link_count
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def id_card_image(request, link_path, image_name):
    response = HttpResponse(content_type='image/jpeg')
    img = Image.open(f'media/{link_path}/{image_name}')
    img.save(response, 'jpeg')
    return response