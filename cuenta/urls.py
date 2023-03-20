from rest_framework import routers
from django.urls import path, include

from cuenta import views

router = routers.DefaultRouter()
router.register(r'', views.CuentaAPIView,basename='')

urlpatterns =[
    path('', include(router.urls)),
]