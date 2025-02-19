from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Record
import json



def home(request):
    return render(request, 'main/index.html')

def gardens(request):
    return render(request, 'main/gardens.html')


def garden_details(request):
    return render(request, 'main/garden-details.html', {'garden_name': 'Garden 1'})




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




def delete_record(request, record_id):
    record = Record.objects.get(id=record_id)
    record.delete()
    return JsonResponse({'success': True})

"""def main_view(request):
    records = Record.objects.all()
    items = []
    for record in records:
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        record_data = record.data  # Ensure we're modifying a copy of the data, not the original
        record_data['timestamp'] = timestamp  # Ensure timestamp is always present
        items.append(record_data)
    return render(request, 'main/main.html', {'items': items, 'records': records})"""