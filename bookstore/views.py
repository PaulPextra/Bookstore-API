from . models import Book
from . serializers import BookSerializer, BookDetailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='POST', request_body=BookSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def add_book(request):
    
    if request.method == 'POST':
        
        serializer_class = BookSerializer(data=request.data)
        
        if serializer_class.is_valid():
            
            book_obj = Book.objects.create(**serializer_class.validated_data)
            
            serializer = BookSerializer(book_obj)
        
            context = {
                'status': True,
                'message': 'Success',
                'data': serializer.data
            }
        
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context = {
                'status': False,
                'message': 'Failed',
                'data': serializer_class.errors
            }
        
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def book_list(request):
    
    if request.method == 'GET':
        
        book_obj = Book.objects.all()
        
        serializer_class = BookSerializer(book_obj, many=True)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
    
        
@api_view(['GET'])
def search_by_id(request, book_id):
    
    try:
        book_obj = Book.objects.get(id=book_id,)
        
    except Book.DoesNotExist:
        
        context = {
            'status': False,
            'message': 'Book does not exist.'
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        
        serializer_class = BookDetailSerializer(book_obj)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }

        return Response(context, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def search_by_category(request, category):
    
    try:
        book_obj = Book.objects.filter(category__name=category)
        
    except Book.DoesNotExist:
        
        context = {
            'status': False,
            'message': 'Book does not exist.'
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        
        serializer_class = BookSerializer(book_obj, many=True)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }

        return Response(context, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def search_by_author(request, author):
    
#     try:
#         book_obj = Book.objects.filter(author__name=author)
        
#     except Book.DoesNotExist:
        
#         context = {
#             'status': False,
#             'message': 'Book does not exist.'
#         }
#         return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'GET':
        
#         serializer_class = BookSerializer(book_obj, many=True)
        
#         context = {
#             'status': True,
#             'message': 'Success',
#             'data': serializer_class.data
#         }

#         return Response(context, status=status.HTTP_200_OK)
