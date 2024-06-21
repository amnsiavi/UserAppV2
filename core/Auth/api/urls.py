from django.urls import path
from Auth.api.views import (get_users_list,get_user,UsersView,delete_user)



urlpatterns = [
    path('list/',get_users_list,name='get_user_list'),
    path('<int:pk>/',get_user),
    path('create/',UsersView.as_view(),name='create_user'),
    path('delete/<int:pk>',delete_user,name='delete_user'),
]
