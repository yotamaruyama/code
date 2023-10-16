from rest_framework import serializers
from dataclasses import dataclass
from occupancy_rate.models import MachineData

class MachineDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MachineData
        fields = ('timestamp', 'is_operational')
        extra_kwargs = {
            'timestamp': {
                'format': '%Y-%m-%d %H:%M:%S',
            },
            'is_operational': {
                'help_text': 'Whether the machine is operational or not',
            }
        }


