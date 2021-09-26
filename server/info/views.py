from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Link, Template, Customer
from .serializers import TemplateSerializer, LinkSerializer, CustomerSerializer



# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def template(request):
    partner = request.user.partner

    if request.method == 'GET':
        # 템플릿 목록 조회
        templates = Template.objects.filter(partner=partner)
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 템플릿 생성
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(partner=request.user.partner)
            data = {
                'success': True
            }
            return Response(data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def template_detail(request, template_id):
    template = get_object_or_404(Template, pk=template_id)

    if template.partner != request.user.partner:
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # 템플릿 상세 조회
        serializer = TemplateSerializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        # 템플릿 수정
        serializer = TemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 템플릿 삭제
        template.delete()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def link(request):
    partner = request.user.partner

    if request.method == 'GET':
        # 링크 목록 조회
        links = Link.objects.filter(partner=partner)
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # 링크 생성
        if request.data.get('customers'):
            customers = [{'name': name} for name in request.data.get('customers')]
        else:
            data = {
                "customers": [
                    "이 필드는 필수 항목입니다."
                ]
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            link = serializer.save(partner=partner)
            for customer in customers:
                serializer = CustomerSerializer(data=customer)
                if serializer.is_valid():
                    serializer.save(link=link)
                    data = {
                        'success': True,
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    link.delete()
                    data = {
                        "customers": [
                            "유효하지 않은 데이터입니다."
                        ]
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def link_detail(request, link_id):
    link = get_object_or_404(Link, pk=link_id)

    if not link.manage_users.filter(pk=request.user.pk).exists():
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
@permission_classes([IsAuthenticated])
def customer(request, link_id):
    link = get_object_or_404(Link, pk=link_id)

    if not link.manage_users.filter(pk=request.user.pk).exists():
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # 해당 링크의 고객정보 확인
        customers = link.customer_set.all()
        serializers = CustomerSerializer(customers, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    link = customer.link
    template = link.template

    if request.method == 'PATCH':
        # 고객 정보 수정
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
