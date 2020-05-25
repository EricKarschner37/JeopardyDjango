from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/buzzer/', consumers.BuzzerConsumer),
    path(r'ws/buzzer/host/', consumers.HostConsumer),
    path(r'ws/buzzer/server/', consumers.ServerConsumer),
]
