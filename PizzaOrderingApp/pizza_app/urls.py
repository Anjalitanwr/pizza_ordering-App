from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('order/', PlaceOrderAPIView.as_view(), name='place_order'),
    path('api/login/',LoginAPIView.as_view(), name='place_order'),
    path('api/logout/',LogoutAPIView.as_view(), name='place_order'),
    path('api/register/',RegisterAPIView.as_view(), name='place_order'),

]