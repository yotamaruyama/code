from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from .models import MachineData
from datetime import timedelta
from django.shortcuts import render
import json  # 追加

class MachineDataView(View):
    def get(self, request, *args, **kwargs):
        time_scale = request.GET.get('time_scale', 'hour')  # Default to 'hour'
        
        # Define timeframes and limits for different scales
        time_scale_map = {
            'hour': (60, 24 * 60),  # 1 hour, max: 24 hours
            'day': (24 * 60, 7 * 24 * 60),  # 1 day, max: 7 days
            'month': (30 * 24 * 60, 30 * 24 * 60)  # 1 month, max: 1 month
        }
        
        # Initialize operational rate dictionary
        rate_dict = {}
        
        # Get the timeframe and max_limit based on the user's choice
        timeframe, max_limit = time_scale_map.get(time_scale, (60, 24 * 60))
        
        # Calculate operational rate
        for i in range(0, max_limit, timeframe):
            time_end = timezone.now() - timedelta(minutes=i)
            time_start = time_end - timedelta(minutes=timeframe)
            subset_data = MachineData.objects.filter(timestamp__gt=time_start, timestamp__lte=time_end)
            
            if subset_data.exists():
                operational_rate = subset_data.filter(is_operational=True).count() / subset_data.count()
                rate_dict[time_end.strftime('%Y-%m-%d %H:%M:%S')] = operational_rate * 100  # Convert to percentage
        
        # Create the response data
        data = {
            'labels': list(rate_dict.keys()),
            'values': list(rate_dict.values()),
        }

        # デバッグ用出力
        print("rate_dict:", json.dumps(rate_dict))
        print("data:", json.dumps(data))
        
        # Acceptヘッダーを確認してレスポンス形式を決定
        accept_header = request.META.get('HTTP_ACCEPT', '')
        
        if 'application/json' in accept_header:
            return JsonResponse(data)
        else:
            return render(request, 'occupancy_rate/occupancy_rate.html', {'data': data})