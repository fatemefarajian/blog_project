from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comment/', views.post_comment, name='comments'),
    path('ticket/', views.ticket, name='tickets'),
    path('success_ticket/', views.success_ticket, name='success_ticket'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_post/', views.create_post, name='create_post'),
    path('profile/create_post/<post_id>', views.edit_post, name='edit_post'),
    path('profile/delete_post/<post_id>', views.delete_post, name='delete_post'),
    path('profile/delete_image/<img_id>', views.delete_image, name='delete_image'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.log_out, name='logout'),


]