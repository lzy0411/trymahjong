from django.urls import path
from django.conf.urls import url

from mahjong import views

urlpatterns = [
    path('', views.lobby, name='home'),
    path('chat/<str:room_name>', views.room, name='room'),
    path('chat/', views.index, name='index'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('lobby', views.lobby, name='lobby'),
    path('createroom', views.create_room, name='createroom'),
    path('joinroom/<int:room_name>/', views.join_room, name='joinroom'),
    path('initialize_game', views.initialize_game,name = 'initialize_game'),
    path('game_instruction', views.game_instruction, name='game_instruction'),
    path('refresh_game_test', views.refresh_game_test, name='refresh_game_test'),
    path('refresh_game/<int:game_id>/<str:message>', views.refresh_game, name='refresh_game'),
    path('discard_tile_grab', views.discard_tile_grab, name='discard_tile_grab'),
    path('discard_tile_grab/<int:discard_tile_id>/<int:game_id>', views.discard_tile_grab_with_id, name='discard_tile_grab_with_id'),
    path('verify_win',views.verify_win,name = 'verify_win'),
    path('triple_tile', views.triple_tile, name='triple_tile'),
    path('win_game', views.win_game, name='win_game'),
    path('win_game/<int:game_id>', views.win_game_redirect, name='win_game/'),
    path('eat_tile', views.eat_tile, name='eat_tile')

    # path('global_action', views.global_action, name='global'),
    # path('follower', views.follower_action, name='follower'),
    # path('profile', views.profile, name='profile'),
    # path('logout', views.logout_action, name='logout'),

    # path('othersProfile/<str:username>', views.others_profile, name='othersProfile'),
    # path('othersProfile', views.others_profile_null, name='othersProfile'),
    # path('follow/<int:id>',views.follow_action,name = 'follow'),
    # path('add-comment', views.add_comment, name='add-comment'),
    # path('add-post', views.add_post, name='add-post'),
    # path('photo/<int:id>', views.get_photo, name='photo'),
    # path('refresh-global', views.refresh_global),
    # path('refresh-follower', views.refresh_follower),

]