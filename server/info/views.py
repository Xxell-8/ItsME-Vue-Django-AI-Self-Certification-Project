from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Link, Template
from .serializers import TemplateSerializer, LinkSerializer



# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def link(request):
    if request.method == 'GET':
        # 링크 목록 조회
        links = get_list_or_404(Link)
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # 링크 생성
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(partner=request.user.partner)
            data = {
                'success': True
            }
            return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def link_detail(request, link_id):
    link = get_object_or_404(Link, pk=link_id)

    if request.method == 'GET':
        # 링크 상세 조회
        serializer = LinkSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        # 링크 수정
        serializer = LinkSerializer(link, data=request.data)
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
    

def customer(request):
    pass


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def template(request):
    if request.method == 'GET':
        # 템플릿 목록 조회
        templates = get_list_or_404(Template)
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

    if request.method == 'GET':
        # 템플릿 상세 조회
        serializer = TemplateSerializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        # 템플릿 수정
        serializer = TemplateSerializer(template, data=request.data)
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