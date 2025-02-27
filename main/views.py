from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now, timedelta
from .models import Garden, Plant, SensorData  
import json
from django.contrib.auth.models import User 
from django.shortcuts import redirect, render

def home(request):
    return render(request, 'main/index.html')

def gardens(request):
    return render(request, 'main/gardens.html')

def garden_details(request):
    plants = Plant.objects.all()
    return render(request, 'main/garden-details.html', {
        'garden_name': 'Garden 1',
        'plants': plants
    })


def add_plant(request):
    return render(request, 'main/add_plant.html')

@csrf_exempt 
def receive_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data

            # Get the hardware ID from the request
            hardware_id = data.get("hardware_id")  
            if not hardware_id:
                return JsonResponse({"success": False, "error": "Hardware ID is required"}, status=400)

            try:
                plant = Plant.objects.get(hardware_id=hardware_id)  # Retrieve the correct plant
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
    plant = get_object_or_404(Plant, id=plant_id)
    try:
        latest = SensorData.objects.filter(plant=plant).order_by('-timestamp').first()

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


def plant_data(request, plant_id):
    """ Fetch sensor data for a specific plant with time filtering """
    plant = get_object_or_404(Plant, id=plant_id)

    # Get time range from request (default: "week")
    time_range = request.GET.get("time_range", "week")

    # Define time filtering
    time_filter = {
        "hour": now() - timedelta(hours=1),
        "day": now() - timedelta(days=1),
        "week": now() - timedelta(weeks=1),
        "month": now() - timedelta(weeks=4),
    }.get(time_range, now() - timedelta(weeks=1))

    # Fetch sensor data within the selected time range
    records = SensorData.objects.filter(plant=plant, timestamp__gte=time_filter).order_by('-timestamp')

    # Format the response
    items = []
    for record in records:
        items.append({
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": record.temperature,
            "humidity": record.humidity,
            "soil_moisture": record.soil_moisture,
            "light": record.light,
        })


    return JsonResponse({"items": items})


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
        garden = Garden.objects.get_or_create(user=user, defaults={"name": "Default Garden"})
        # Create and save the new plant
        Plant.objects.create(
            garden=garden,
            name=plant_name,
            species=plant_type,
            hardware_id=hardware_id
        )

        return redirect("gardens")

    return render(request, "main/add_plant.html")

def plant_dashboard(request, plant_id):
    """ Display a dashboard for a specific plant """
    plant = get_object_or_404(Plant, id=plant_id)

    # Fetch all sensor data linked to this plant
    sensor_data = SensorData.objects.filter(plant=plant).order_by('-timestamp')

    return render(request, "main/plant_dashboard.html", {"plant": plant, "sensor_data": sensor_data})

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