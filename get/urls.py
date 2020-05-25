from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetView.as_view(), name='get'),
]
