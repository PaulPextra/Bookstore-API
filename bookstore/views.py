from . models import Author, Book
from . serializers import BookSerializer, BookDetailSerializer, AddBookSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='POST', request_body=AddBookSerializer())
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

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=BookSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def update_book(request, book_title):
    
    try:
        book_obj = Book.objects.get(title=book_title)
        
    except Book.DoesNotExist:
        
        context = {
            'status': False,
            'message': 'Book does not exist.'
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        
        serializer_class = BookSerializer(book_obj)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }

        return Response(context, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        
        serializer_class = BookSerializer(book_obj, 
                                                data=request.data, 
                                                partial=True)
        
        if serializer_class.is_valid():
            
            serializer_class.save()
            
            context = {
                'status': True,
                'message': 'Success',
                'data': serializer_class.data
            }
            
            return Response(context, status=status.HTTP_202_ACCEPTED)
        
        else:
            context = {
                'status': False,
                'message': 'Failed',
                'error': serializer_class.errors
            }
            
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        
        book_obj.delete()

        data = {
            'status'  : True,
            'message' : 'Deleted Successfully'
        }

        return Response(data, status = status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def fetch_books(request):
    
    if request.method == 'GET':
        
        book_obj = Book.objects.all().order_by('title')
        
        serializer_class = BookSerializer(book_obj, many=True)
        
        context = {
            'status': True,
            'message': 'Success',
            'data': serializer_class.data
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
        
@api_view(['GET'])
def search_by_title(request, title):
    
    try:
        book_obj = Book.objects.get(title=title)
        
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


@api_view(['GET'])
def search_by_author(request, book_author):
    try:
        book_obj = Book.objects.filter(author__name=book_author)
        
    except Book.DoesNotExist:
        
        context = {
            'status': False,
            'message': 'Author not found.'
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
