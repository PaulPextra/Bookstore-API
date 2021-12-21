from . models import Category
from . serializers import CategoryDetailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def category(request):
    if request.method == 'GET':
        category_obj = Category.objects.all().order_by('name')
        serializer_class = CategoryDetailSerializer(category_obj, many=True)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)