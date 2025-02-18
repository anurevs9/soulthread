from django.urls import path
from . import views
from .views import FollowUnfollowView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/view/', views.view_post, name='view_post'),
    path('upload/media/', views.upload_media, name='upload_media'),
    path('messages/', views.messages_view, name='messages'),
    path('forums/', views.forums_view, name='forums'),

    path('about/', views.about, name='about'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', views.contact, name='contact'),


    path('forums/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('friends/', views.friends, name='friends'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('media/', views.media, name='media'),
    path('settings/', views.settings_view, name='settings'),
    path('follow-user/', views.follow_user, name='follow_user'),
    path('follow/', FollowUnfollowView.as_view(), name='follow_unfollow'),
    path('messages/send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('api/stories/', views.api_stories, name='api_stories'),
    path('api/suggestions/', views.api_suggestions, name='api_suggestions'),
    path('api/recommendations/', views.api_recommendations, name='api_recommendations'),

    path('post/create/', views.create_post, name='create_post'),

]