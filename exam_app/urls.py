from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.quotes_page),
    path('add_quote', views.add_quote),
    path('delete_quote/<int:quote_id>', views.delete_quote),
    path('myaccount/<int:user_id>', views.edit_acc),
    path('validate/<int:user_id>', views.edit_validate),
    path('user/<int:user_id>', views.user_page),
    path('likes/<int:quote_id>', views.likes)
    
]