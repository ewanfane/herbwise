from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Garden, Plant, SensorData  
import json
from django.contrib.auth.models import User 
from django.shortcuts import redirect, render

def home(request):
    return render(request, 'main/index.html')

def gardens(request):
    return render(request, 'main/gardens.html')

def garden_details(request):
    return render(request, 'main/garden-details.html', {'garden_name': 'Garden 1'})

def add_plant(request):
    return render(request, 'main/add_plant.html')

@csrf_exempt 
def receive_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data

            # Get the plant ID from the incoming data
            plant_id = data.get("plant_id")  
            if not plant_id:
                return JsonResponse({"success": False, "error": "Plant ID is required"}, status=400)

            try:
                plant = Plant.objects.get(id=plant_id)  # Retrieve the correct plant
            except Plant.DoesNotExist:
                return JsonResponse({"success": False, "error": "Plant not found"}, status=404)

            # Store the sensor data correctly in SensorData model
            record = SensorData.objects.create(
                plant=plant,
                temperature=data.get("temperature", 0),
                humidity=data.get("humidity", 0),
                soil_moisture=data.get("soil_moisture", 0),
                light=data.get("light", 0)
            )

            return JsonResponse({"success": True, "id": record.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"success": False, "error": "Only POST requests allowed"}, status=405)

def latest_record(request, plant_id):
    """ Fetch the latest sensor data for a specific plant """
    try:
        latest = SensorData.objects.filter(plant_id=plant_id).order_by('-timestamp').first()
        if latest:
            return JsonResponse({
                "timestamp": latest.timestamp,
                "temperature": latest.temperature,
                "humidity": latest.humidity,
                "soil_moisture": latest.soil_moisture,
                "light": latest.light
            })
        return JsonResponse({"error": "No data available"}, status=404)
    except Plant.DoesNotExist:
        return JsonResponse({"error": "Plant not found"}, status=404)


def add_plant(request):
    """ Handles form submission for creating a new plant. """
    if request.method == "POST":
        plant_name = request.POST.get("plant_name")  # Get plant name from form
        plant_type = request.POST.get("plant_type")  # Get plant type
        hardware_id = request.POST.get("hardware_id")  # Get hardware ID

        user = User.objects.first()  # Get any existing user
        if not user:
            user = User.objects.create_user(username="defaultuser", password="password123")
        # Ensure user has a garden
        garden = Garden.objects.filter(user=user, name="Default Garden").first()
        garden, created = Garden.objects.get_or_create(user=user, defaults={"name": "Default Garden"})
        # Create and save the new plant
        Plant.objects.create(
            garden=garden,
            name=plant_name,
            species=plant_type,
            hardware_id=hardware_id
        )

        return redirect("gardens")

    return render(request, "main/add_plant.html")

@csrf_exempt
def delete_record(request, record_id):
    """ Delete a specific sensor data record """
    try:
        record = SensorData.objects.get(id=record_id)
        record.delete()
        return JsonResponse({'success': True})
    except SensorData.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)

"""def main_view(request):
    records = Record.objects.all()
    items = []
    for record in records:
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        record_data = record.data  # Ensure we're modifying a copy of the data, not the original
        record_data['timestamp'] = timestamp  # Ensure timestamp is always present
        items.append(record_data)
    return render(request, 'main/main.html', {'items': items, 'records': records})"""