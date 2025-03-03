from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now, timedelta
from .models import Garden, HousePlant, Plant, SensorData  
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'main/index.html')

@login_required
def gardens(request):
    user_gardens = Garden.objects.filter(user=request.user)  # Only show the logged-in user's gardens
    return render(request, 'main/gardens.html', {"gardens": user_gardens})
 


@login_required
def garden_details(request, garden_id):
    garden = get_object_or_404(Garden, id=garden_id, user=request.user)  # Ensure the user owns the garden
    plants = Plant.objects.filter(garden=garden) 
    return render(request, 'main/garden-details.html', {'garden': garden, 'plants': plants})



@login_required
def add_plant(request):
    """ Handles form submission for creating a new plant. """
    if request.method == "POST":
        plant_name = request.POST.get("plant_name")  # Get plant name from form
        plant_type = request.POST.get("house_plant_type")  # Get plant type
        hardware_id = request.POST.get("hardware_id")  # Get hardware ID
        
   
        garden, created = Garden.objects.get_or_create(
            user=request.user, 
            defaults={"name": f"{request.user.username}'s Garden"}
        )
        
        # Create and save the new plant
        Plant.objects.create(
            garden=garden,
            name=plant_name,
            houseplant_type_id=request.POST.get("houseplant_type"),
            hardware_id=hardware_id
        )

        return redirect("gardens")
    
    houseplants = HousePlant.objects.all()
    return render(request, "main/add_plant.html", {"houseplants": houseplants})



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
        record_data = {
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": record.temperature,
            "humidity": record.humidity,
            "soil_moisture": record.soil_moisture,
            "light": record.light,
        }
        
        # Add plant thresholds to each data point if houseplant_type exists
        if plant.houseplant_type:
            record_data["thresholds"] = {
                "temperature": {
                    "min": plant.houseplant_type.min_temperature,
                    "max": plant.houseplant_type.max_temperature,
                    "preferred": plant.houseplant_type.preferred_temperature
                },
                "humidity": {
                    "min": plant.houseplant_type.min_humidity,
                    "max": plant.houseplant_type.max_humidity,
                    "preferred": plant.houseplant_type.preferred_humidity
                },
                "soil_moisture": {
                    "min": plant.houseplant_type.min_soil_moisture,
                    "max": plant.houseplant_type.max_soil_moisture,
                    "preferred": plant.houseplant_type.preferred_soil_moisture
                },
                "light": {
                    "min": plant.houseplant_type.min_light,
                    "max": plant.houseplant_type.max_light,
                    "preferred": plant.houseplant_type.preferred_light
                }
            }
        
        items.append(record_data)

    # Add plant metadata
    plant_info = {"id": plant.id, "name": plant.name, "hardware_id": plant.hardware_id}
    
    if plant.houseplant_type:
        plant_info["type"] = plant.houseplant_type.name

    return JsonResponse({ "items": items, "plant": plant_info
    })


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

@login_required
@csrf_exempt  
def create_garden(request):
    if request.method == "POST":
        garden_name = request.POST.get("garden_name")
        if garden_name:
            garden = Garden.objects.create(
                user=request.user,
                name=garden_name
            )
            return redirect("gardens")
    return JsonResponse({"success": False}, status=400)