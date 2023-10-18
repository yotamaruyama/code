from django.apps import AppConfig
import threading
class OcccupancyRateApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'occcupancy_rate_api'
    def ready(self):
        from occupancy_rate.models import MachineData  # モデルを動的にインポート
        thread = threading.Thread(target=self.start_socket_communication)
        thread.daemon = True
        thread.start()

    def start_socket_communication(self):
        from occcupancy_rate_api.socket_code import main  # socket_code.py として保存した関数をインポート
        main()