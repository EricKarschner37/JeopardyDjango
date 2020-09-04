from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:game_num>/', views.game, name='host'),
    path('<int:game_num>/double/', views.double, name='double'),
    path('<int:game_num>/final/', views.final, name='final'),
]
