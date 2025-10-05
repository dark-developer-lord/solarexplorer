from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_view, name='logout'),
    path('forum/', views.forum_main, name='forum_main'),
    path('forum/<int:thread_id>/', views.forum_thread, name='forum_thread'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('analytics/', views.nasa_analytics, name='nasa_analytics'),
    path('demo/', views.ai_demo, name='ai_demo'),
]