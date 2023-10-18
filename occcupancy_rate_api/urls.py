from django.urls import path,include
from rest_framework import routers

#from .views import MachineDataViewSet
#from .views import SocketCommunicationView

defaultRouter = routers.DefaultRouter()

#defaultRouter.register('MachineData', MachineDataViewSet)

urlpatterns = [
    path('occcupancy_rate_api/', include(defaultRouter.urls)),
    #path('occcpancy_rate_api/', SocketCommunicationView.as_view(),name='socket'),

]