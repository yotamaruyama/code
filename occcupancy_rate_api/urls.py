from django.urls import path,include
from rest_framework import routers

from .views import MachineDataViewSet

defaultRouter = routers.DefaultRouter()

defaultRouter.register('machine_data', MachineDataViewSet)

urlpatterns = [
    path('occcupancy_rate_api/', include(defaultRouter.urls)),

]