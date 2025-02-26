from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Garden, Plant, SensorData  
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'main/index.html')

@login_required
def gardens(request):
    return render(request, 'main/gardens.html')



@login_required
def garden_details(request):
    plants = Plant.objects.all()
    return render(request, 'main/garden-details.html', {
        'garden_name': 'Garden 1',
        'plants': plants
    })



@login_required
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

@login_required
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


@login_required
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

@login_required
def plant_dashboard(request, plant_id):
    """ Display a dashboard for a specific plant """
    plant = get_object_or_404(Plant, id=plant_id)

    # Fetch all sensor data linked to this plant
    sensor_data = SensorData.objects.filter(plant=plant).order_by('-timestamp')

    return render(request, "main/plant_dashboard.html", {"plant": plant, "sensor_data": sensor_data})

@login_required
@csrf_exempt
def delete_record(request, record_id):
    """ Delete a specific sensor data record """
    try:
        record = SensorData.objects.get(id=record_id)
        record.delete()
        return JsonResponse({'success': True})
    except SensorData.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)

