# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    #as_asgi instantiate an instance of our consumer for each user-connection
    #re_path(r'chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'mahjong/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'mahjong/joinroom/(?P<room_name>\w+)/$', consumers.JoinRoomConsumer.as_asgi()),
    re_path(r'mahjong/game/(?P<room_name>\w+)/$', consumers.GameConsumer.as_asgi()),
]
