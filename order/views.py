from .serializers import OrderSerializer
from .models import Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body=OrderSerializer())
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == 'GET':
        
        order_obj = Order.objects.all().order_by('id')
        
        serializer_class = OrderSerializer(order_obj, many=True)
        
        context = {
            'status': True,
            'message': 'success',
            'data': serializer_class.data
        }

        return Response(context, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer_class = OrderSerializer(data=request.data)
        
        if serializer_class.is_valid():
            
            order = Order.objects.create(**serializer_class._validated_data)
            order.save()
            
            context = {
                'status': True,
                'message': 'Order placed successfully',
                'data': serializer_class.data
            }

            return Response(context, status=status.HTTP_201_CREATED)
        else:
            
            context = {
                'status': False,
                'message': 'Invalid data',
                'error': serializer_class.errors
            }
            
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
      
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=OrderSerializer())      
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])           
def order_detail(request, order_id):
    
    try:
        order_obj = Order.objects.get(id=order_id)
    
    except Order.DoesNotExist:
        
        data = {
            'status'  : False,
            'message' : "Does not exist"
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if order_obj.user != request.user:
        
        raise PermissionDenied("You do not have permission to perform this action")
    
    if request.method == 'GET':
        
        serializer_class = OrderSerializer(order_obj)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        
        serializer_class = OrderSerializer(order_obj, data=request.data, partial=True) 

        if serializer_class.is_valid():
        
            serializer_class.save()

            data = {
                'status'  : True,
                'message' : 'Successful',
                'data' : serializer_class.data,
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:
            data = {
                'status'  : False,
                'message' : 'Unsuccessful',
                'error' : serializer_class.errors
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        
        order_obj.delete()

        data = {
            'status'  : True,
            'message' : 'Deleted Successfully'
        }

        return Response(data, status = status.HTTP_204_NO_CONTENT)









