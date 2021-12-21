from .models import Cart
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from .serializers import CartSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model

User = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body=CartSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated]) 
def cart(request):
    
    user = request.user
    
    if user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        cart_obj = Cart.objects.filter(user=request.user)
        serializer_class = CartSerializer(cart_obj, many=True)
        
        context = {
            'status': 'True',
            'message': 'Success',
            'data': serializer_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer_class = CartSerializer(data=request.data)
        
        if serializer_class.is_valid():
            
            if 'user' in serializer_class.validated_data.keys():
                serializer_class.validated_data.pop('user')
            
            cart = Cart.objects.create(**serializer_class.validated_data, user=request.user)
            serializer = CartSerializer(cart)
            
            context = {
                'status': True,
                'message': 'Success',
                'data': serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            
            context = {
                'status': False,
                'error': serializer_class.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=CartSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def cartitem(request, cart_id):
    
    user = request.user
    
    if user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        cart = Cart.objects.get(id=cart_id)
        
    except Cart.DoesNotExist:
        
        context = {
            'status'  : False,
            'message' : 'Empty Cart'
        }

        return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializers_class = CartSerializer(cart)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializers_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        
        serializers_class = CartSerializer(cart, data=request.data, partial=True)
        
        if serializers_class.is_valid():
            
            serializers_class.save()
            
            context = {
                'status': True,
                'message': 'Success',
                'data': serializers_class.data
            }
            return Response(context, status=status.HTTP_202_ACCEPTED)
        
        else:
            
            context = {
                'status': False,
                'message': 'Failed',
                'error': serializers_class.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        
        cart.delete()

        context = {
            'status'  : True,
            'message' : 'Deleted Successfully'
        }

        return Response(context, status=status.HTTP_204_NO_CONTENT)
    