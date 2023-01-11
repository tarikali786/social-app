from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('settings',views.settings,name='settings'),
    path('follow',views.follow,name='follow'),
    path('logout',views.logout,name='logout'),
    path('upload',views.upload,name ='upload'),
    path('search',views.search,name='search'),
    path('like-post',views.likePost,name='like-post'),
    path('profile/<str:pk>/',views.profile,name='profile'),
    
    
]

