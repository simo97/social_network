from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signin', views.signin_view, name='signin'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('panel', views.panel_view, name='panel'),
    path('friendships', views.list_friendship_view, name='list_friendships'),
    path('friendships/create/<pk>',
         views.create_friendship_view,
         name='create_friendship'),
    path('friendships/accept/<pk>',
         views.accept_friendship_view,
         name='accept_friendship'),
    path('friendships/delete/<pk>',
         views.delete_friendship_view,
         name='delete_friendship'),
    path('users', views.list_users_view, name='list_users'),
    path('friends', views.list_friends_view, name='list_friends'),
    path('friends/delete/<pk>', views.delete_friend_view,
         name='delete_friend'),
    path('notifications/delete/<pk>',
         views.delete_notification_view,
         name='delete_notification'),
    path('notifications',
         views.list_notifications_view,
         name='list_notifications'),
    path('users/<pk>', views.user_details_view, name='user_details'),
    path('messages/send/<pk>', views.send_message_view, name='send_message'),
    path('messages', views.messages_view, name='messages'),
    path('messages/<pk>', views.get_messages_view, name='get_messages'),
    path('messages/delete/<pk>',
         views.delete_message_view,
         name='delete_message'),
    path('articles/create', views.create_article_view, name='create_article'),
    path('articles', views.articles_view, name='articles'),
    path('articles/delete/<pk>',
         views.delete_article_view,
         name='delete_article'),
    path('articles/liked/<pk>', views.liked_article_view,
         name='liked_article'),
    path('comments/create/<pk>',
         views.create_comment_view,
         name='create_comment'),
    path('articles/<pk>', views.get_comments_view, name='get_comments'),
    path('comments/delete/<pk>',
         views.delete_comment_view,
         name='delete_comment'),
    path('articles/share/<pk>',
         views.share_article_view,
         name='share_article'),
]
