from django.contrib.auth import (get_user_model, 
                                 authenticate)
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.hashers import (make_password, 
                                         check_password)
from . serializers import (CustomUserSerializer, 
                           ChangePasswordSerializer,
                           UserProfileSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (api_view, 
                                       authentication_classes, 
                                       permission_classes)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import (IsAuthenticated, 
                                        IsAdminUser,)
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['POST'])
def add_user(request):
    
    """ Allows the user to be able to sign up on the platform """

    if request.method == 'POST':
        
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():

            # hash password
            serializer.validated_data['password'] = make_password(serializer.validated_data['password']) # hash the given password
            
            user = User.objects.create(**serializer.validated_data)
            
            serializer_class = CustomUserSerializer(user)
            
            data = {
                'status'  : True,
                'message' : 'Successful',
                'data' : serializer_class.data
            }

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : 'Unsuccessful',
                'error' : serializer.errors,
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def get_user(request):
    
    """Allows the admin to see all users (both admin and normal users) """
    
    if request.method == 'GET':
        
        user = User.objects.filter(is_active=True)
    
        serializer_class = CustomUserSerializer(user, many=True)
        
        data = {
                'status'  : True,
                'message' : 'Successful',
                'data' : serializer_class.data,
            }

        return Response(data, status=status.HTTP_200_OK)

        
       
# Get the detail of a single user by their ID
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=UserProfileSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    
    """Allows the logged in user to view their profile, edit or deactivate account. 
    Do not use this view for changing password or resetting password"""
    
    try:
        user = User.objects.get(id=request.user.id, is_active=True)
        
    except User.DoesNotExist:
        
        data = {
            'status'  : False,
            'message' : 'Does not exist'
        }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        serializer_class = UserProfileSerializer(user)
        
        data = {
            'status'  : True,
            'message' : 'Successful',
            'data' : serializer_class.data,
        }

        return Response(data, status=status.HTTP_200_OK)

    # Update the profile of the user
    elif request.method == 'PUT':
        
        serializer_class = UserProfileSerializer(user, data=request.data, partial=True) 

        if serializer_class.is_valid():
            
            if 'password' in serializer_class.validated_data.keys():
                
                raise ValidationError(detail='Cannot change password with this view')
            
            serializer_class.save()

            data = {
                'status'  : True,
                'message' : 'Successful',
                'data' : serializer_class.data,
            }

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : 'Unsuccessful',
                'error' : serializer_class.errors,
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # Delete the account
    elif request.method == 'DELETE':
        
        user.is_active = False
        
        user.save()

        data = {
            'status'  : True,
            'message' : 'Deleted Successfully'
        }

        return Response(data, status=status.HTTP_204_NO_CONTENT)

# Setup for user login
@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties = {
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view(['POST'])
def user_login(request):
    
    """Allows users to log in to the platform."""
    
    if request.method == 'POST':
        
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        
        if user is not None:
            
            if user.is_active == True:
                
                try:

                    user_detail = {}
                    user_detail['id'] = user.id
                    user_detail['first_name'] = user.first_name
                    user_detail['last_name'] = user.last_name
                    user_detail['email'] = user.email
                    user_detail['username'] = user.username
                    
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                        'status'  : True,
                        'message' : 'Successful',
                        'data' : user_detail
                    }
                    return Response(data, status=status.HTTP_200_OK)
                
                except Exception as e:
                    
                    raise e
            else:
                
                data = {
                    'status'  : False,
                    'error': 'This account has not been activated'
                }
                
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        else:
            data = {
                'status'  : False,
                'error': 'Please provide a valid username and a password'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
        
@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])   
def reset_password(request):
    
    """Allows users to edit password when logged in"""
    
    user = request.user
    
    if request.method == 'POST':
        
        serializer_class = ChangePasswordSerializer(data=request.data)
        
        if serializer_class.is_valid():
            
            if check_password(serializer_class.validated_data['old_password'], user.password):
                
                if serializer_class.validate_new_password():
                    
                    user.set_password(serializer_class.validated_data['new_password'])
                    
                    user.save()
                    
                    data = {
                        'status'  : True,
                        'message': 'Successfully saved password'
                    }
                    
                    return Response(data, status=status.HTTP_202_ACCEPTED)
                
                else:
                    
                    data = {
                        'status'  : False,
                        'error': 'Please enter matching passwords'
                    }
                    
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)   
            else:
                
                data = {
                    'status'  : False,
                    'error': 'Incorrect password'
                }
                
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)   
        else:
            
            data = {
                'status'  : False,
                'error': serializer_class.errors
            }
            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)   
        
@swagger_auto_schema(methods=['DELETE'], request_body=CustomUserSerializer())
@api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_detail(request, user_id):
    
    try:
        user = User.objects.get(id=user_id, is_active=True)
    
    except User.DoesNotExist:
        
        data = {
            'status'  : False,
            'message' : 'Does not exist'
        }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        serializer_class = CustomUserSerializer(user)
        
        data = {
                'status'  : True,
                'message' : 'Successful',
                'data' : serializer_class.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    # Delete the account
    elif request.method == 'DELETE':
        
        user.is_active = False
        
        user.save()

        data = {
            'status'  : True,
            'message' : 'Deleted Successfully'
        }

        return Response(data, status = status.HTTP_204_NO_CONTENT)