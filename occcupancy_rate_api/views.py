from rest_framework import viewsets
from occupancy_rate.models import MachineData
from .serializers import MachineDataSerializer  # シリアライザのインポートを確認

class MachineDataViewSet(viewsets.ModelViewSet):
    queryset = MachineData.objects.all()
    serializer_class = MachineDataSerializer