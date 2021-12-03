from . models import Category
from . serializers import CategorySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def category(request):
    if request.method == 'GET':
        category_obj = Category.objects.all().order_by('-created_at')
        serializer_class = CategorySerializer(category_obj, many=True)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)