from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from Auth.permissions import AdminUser, RegularUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
)
from rest_framework import (
    generics, mixins
)
from django.contrib.auth.models import User

from Auth.api.serializer import AuthSerializer

@api_view(['GET'])
@permission_classes([AdminUser|RegularUser, IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_users_list(request):
    instance = User.objects.all()
    serializer = AuthSerializer(instance,many=True)
    
    return Response({
        'data':serializer.data,
        'msg':'Data fetched sucessfully',
        'total':len(serializer.data)
    },status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user(request,pk):
    instance = User.objects.get(pk=pk)
    serializer = AuthSerializer(instance)
    return Response({
        'data':serializer.data,
        'msg':'User Fetched Sucessfully',
    },status=HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([AdminUser, IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_user(request,pk):
    instance = User.objects.get(pk=pk)
    instance.delete()
    return Response({
        'msg':'User Deleted Sucessfully'
    },status=HTTP_200_OK)



class UsersView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin
):
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [AdminUser,IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def put(self,request,*args,**kwargs):
        
        try:
            if len(request.data) == 0:
                return Response({
                    'errors':'Recieved Empty Object'
                },status=HTTP_400_BAD_REQUEST)
            else:
                instance = self.get_object()
                serializer = self.get_serializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'msg':'User Updated',
                        'user':serializer.data
                    },status=HTTP_200_OK)
                else:
                    return Response({
                        'msg':'Updation Failed',
                        'errors':'Invalid Object'
                    },status=HTTP_400_BAD_REQUEST)
                
        except ValidationError as ve:
            return Response({
                'errors':ve.detail,
                'msg':'Updation Failed'
            },status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'errors':str(e),
                'msg':'Updation Failed'
            },status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self,request,*args,**kwargs):
        
        try:
            if len(request.data) == 0:
                return Response({
                    'errors':'Recieved Empty Object',
                    'msg':'Updation Failed'
                },status=HTTP_400_BAD_REQUEST)
            else:
                instance = self.get_object()
                serializer = self.get_serializer(instance,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'msg':'User Updated',
                        'user':serializer.data
                    })
                else:
                    return Response({
                        'msg':'Updation Failed',
                        'errors':'Invalid Object'
                    },status=HTTP_400_BAD_REQUEST)
                
        except ValidationError as ve:
            return Response({
                'errors':ve.detail,
                'msg':'Updation Failed'
            },status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'errors':str(e),
                'msg':'Updation Failed'
            },status=HTTP_500_INTERNAL_SERVER_ERROR)