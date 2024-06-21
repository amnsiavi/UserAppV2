from django.urls import path

from App_User.api.views import get_app_users,create_app_user, AppUserView

urlpatterns = [
    path('list/',get_app_users,name='get_app_users'),
    path('user/create',create_app_user,name='create_user'),
    path('user/<int:pk>',AppUserView.as_view(),name='get_user'),
    
]
