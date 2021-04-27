from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/create', views.create_user),
    path('quotes', views.main_page),
    path('users/login', views.login),
    path('logout', views.logout),
    path('users/add_quote', views.add_quote),
    path('quotes/like/<int:quote_id>', views.like_quote),
    path('quotes/unlike/<int:quote_id>', views.unlike_quote),
    path('user/<int:user_id>', views.user_quotes),
    path('myaccount/<int:user_id>/edit', views.edit_account),
    path('myaccount/<int:user_id>/update', views.update_account),
    path('quotes/delete/<int:quote_id>', views.delete_quote),
]
