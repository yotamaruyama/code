from django.urls import path
from .views import MachineDataView

urlpatterns = [
    path('occupancy_rate/', MachineDataView.as_view(), name='occupancy_rate'),
    # 他のURL設定
]
