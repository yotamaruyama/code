from rest_framework import viewsets
from occupancy_rate.models import MachineData
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MachineDataSerializer  # シリアライザのインポートを確認
"""
import socket
import time
from datetime import datetime,timedelta,timezone
from occupancy_rate.models import MachineData

#tz = pytz.timezone('Asia/Tokyo')
first_run = True
JST = timezone(timedelta(hours=+9))

class SocketCommunicationView(APIView):
    
    @staticmethod
    def one_minutes_timer():
        global first_run
        if first_run:
            first_run = False
            return
        timer1 = time.time()
        while True:
            timer2 = time.time()
            if timer2 - timer1 >= 60:
                break
                
    @staticmethod
    def data(response):
        msg = str(response)
        msg = int(msg[-4:])
        is_operational = (msg == 1)
        return msg, is_operational
                
    def get(self, request):
        ip = "192.168.8.114"
        port = 12345
        is_first_run = True
        try:
            while is_first_run:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(3)
                client_socket.connect((ip, port))
                is_first_run = False

            while True:
                self.one_minutes_timer()
                client_socket.sendall(b"D200")
                response = client_socket.recv(1024).decode()
                msg, is_operational = self.data(response)
                utc_now = datetime.now(timezone.utc)
                base_datetime = utc_now.astimezone(JST)
                base_datetime = base_datetime.strftime("%Y-%m-%d %H:%M:%S")
                MachineData.objects.create(
                    timestamp=base_datetime,
                    is_operational=is_operational
                )
                
        except TimeoutError:
            return Response({"error": "接続要求タイムアウト"}, status=500)
        except ConnectionRefusedError:
            return Response({"error": "サーバから接続が拒否されました。"}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        return Response({"status": "success"})
class MachineDataViewSet(viewsets.ModelViewSet):
    queryset = MachineData.objects.all()
    serializer_class = MachineDataSerializer"""

