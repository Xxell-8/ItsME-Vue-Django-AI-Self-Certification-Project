from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Template
from .serializers import TemplateSerializer

# Create your views here.
def link(request):
    pass


def link_detail(request):
    pass


def client(request):
    pass


@api_view(['GET', 'POST'])
def template(request):
    if request.method == 'GET':
        # 템플릿 목록 조회
        templates = get_list_or_404(Template)
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 템플릿 생성
        pass
    


def template_detail(request):
    pass