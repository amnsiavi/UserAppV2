from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes
)
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework import generics, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Models
from App_User.models import UserAppModel

# Serializer
from App_User.api.serializer import AppUserSerializer

# Permissions
from Auth.permissions import AdminUser, RegularUser

@api_view(['GET'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_app_users(request):
    try:
        instance = UserAppModel.objects.all()
        serializer = AppUserSerializer(instance,many=True)
        return Response({
            'data':serializer.data,
            'total':len(serializer.data)
        },status=HTTP_200_OK)
    except Exception as e:
        return Response({
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)

class AppUserView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    queryset = UserAppModel.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AdminUser,RegularUser, IsAuthenticated]
    
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(),(AdminUser|RegularUser)()]
        elif self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAuthenticated(),AdminUser()]
        else:
            return [IsAuthenticated()]
    
    def get(self,request,*args,**kwargs):
        return Response({
            'data':self.retrieve(request,*args,**kwargs).data,
            'msg':'Fetch Sucessful'
        },status=HTTP_200_OK)
    
    def delete(self,request,*args,**kwargs):
        
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'msg':'Deletion Sucessfull',
                'done':True
            },status=HTTP_200_OK)
        except Exception as e:
            return Response({
                'errors':str(e),
                'msg':'Deletion Failed'
            },status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self,request,*args,**kwargs):
        try:
            if len(request.data) == 0:
                return Response({
                    'errors':'Recieved Empty Object',
                    'msg':'Updation Failed'
                },status=HTTP_400_BAD_REQUEST)
            else:
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'msg':'User Updated',
                        'user':serializer.data
                    },status=HTTP_200_OK)
                else:
                    return Response({
                        'msg':'Invalid Object'
                    },status=HTTP_400_BAD_REQUEST)
                
              
        except ValidationError as ve:
            return Response({
                'msg':'Updattion failed',
                'errors':ve.detail
            },status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'errors':str(e),
                'msg':'Updation Failed'
            },status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'msg':'User Updated',
                    'user':serializer.data
                },status=HTTP_200_OK)
            else:
                return Response({
                    'errors':'Invalid Object'
                },status=HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            return Response({
                'msg':'Invalid Object',
                'errors':ve.detail
            },status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            
            return Response({
                'errors':str(e),
                'msg':'Error'
            },status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated,AdminUser])
@authentication_classes([JWTAuthentication])
def create_app_user(request):
    try:
        if request.user.is_authenticated:
            if len(request.data) == 0:
                return Response({
                    'errors':'Recieced Empty Object'
                },status=HTTP_400_BAD_REQUEST)
            serializer = AppUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'msg':'Reccord Created'
                },status=HTTP_201_CREATED)
            else:
                return Response({
                    'errors':'Invalid Object'
                },status=HTTP_400_BAD_REQUEST)
    except ValidationError as ve:
        return Response({
            'errors':ve.detail
        },status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)