from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Item, Box, Record
import json



def main_view(request):
    records = Record.objects.all()
    items = []
    for record in records:
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        record_data = record.data  # Ensure we're modifying a copy of the data, not the original
        record_data['timestamp'] = timestamp  # Ensure timestamp is always present
        items.append(record_data)
    return render(request, 'main/main.html', {'items': items, 'records': records})



def roulette_view(request):
    
    return render(request, 'main/poker.html')


def roulette_view2(request):
    
    return render(request, 'main/poker2.html')

def roulette_view3(request):
    
    return render(request, 'main/poker3.html')



def delete_record(request, record_id):
    record = Record.objects.get(id=record_id)
    record.delete()
    return JsonResponse({'success': True})



@csrf_exempt 
def receive_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            record = Record.objects.create(data=data)  # Save to database
            return JsonResponse({"success": True, "id": record.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    return JsonResponse({"success": False, "error": "Only POST requests allowed"}, status=405)
