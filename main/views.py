from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now, timedelta
from .models import Garden, HousePlant, Plant, SensorData, GardenVisit  
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
    garden = get_object_or_404(Garden, id=garden_id, user=request.user)
    plants = Plant.objects.filter(garden=garden)

    for plant in plants:
        if plant.houseplant_type:
            # --- Store thresholds as a DICTIONARY, directly usable by JS ---
            plant.thresholds_js = {
                "temperature": {
                    "min": plant.houseplant_type.min_temperature,
                    "max": plant.houseplant_type.max_temperature,
                },
                "humidity": {
                    "min": plant.houseplant_type.min_humidity,
                    "max": plant.houseplant_type.max_humidity,
                },
                "soil_moisture": {
                    "min": plant.houseplant_type.min_soil_moisture,
                    "max": plant.houseplant_type.max_soil_moisture,
                },
                "light": {
                    "min": plant.houseplant_type.min_light,
                    "max": plant.houseplant_type.max_light,
                }
            }
            # --- END CHANGE ---

        latest_data = SensorData.objects.filter(plant=plant).order_by('-timestamp').first()
        plant.needs_attention = False
        # Create attributes to hold highlighted status.  Initialize to False.
        plant.temp_out_of_bounds = False
        plant.humidity_out_of_bounds = False
        plant.moisture_out_of_bounds = False
        plant.light_out_of_bounds = False


        if latest_data:
            if (latest_data.temperature < plant.houseplant_type.min_temperature or
                latest_data.temperature > plant.houseplant_type.max_temperature):
                plant.temp_out_of_bounds = True
                plant.needs_attention = True

            if (latest_data.humidity < plant.houseplant_type.min_humidity or
                latest_data.humidity > plant.houseplant_type.max_humidity):
                plant.humidity_out_of_bounds = True
                plant.needs_attention = True

            if (latest_data.soil_moisture < plant.houseplant_type.min_soil_moisture or
                latest_data.soil_moisture > plant.houseplant_type.max_soil_moisture):
                plant.moisture_out_of_bounds = True
                plant.needs_attention = True

            if (latest_data.light < plant.houseplant_type.min_light or
                latest_data.light > plant.houseplant_type.max_light):
                plant.light_out_of_bounds = True
                plant.needs_attention = True

    #Streak update
    visit, created = GardenVisit.objects.get_or_create(user=request.user, garden=garden)
    visit.update_streak()

    context = {
        'garden': garden,
        'plants': plants,
        'streak': visit.streak,  
    }
    return render(request, 'main/garden-details.html', context)






@login_required
def add_plant(request, garden_id):
    """ Handles form submission for creating a new plant. """
    if request.method == "POST":
        plant_name = request.POST.get("plant_name")  # Get plant name from form
        plant_type = request.POST.get("house_plant_type")  # Get plant type
        hardware_id = request.POST.get("hardware_id")  # Get hardware ID
        
   
        garden = Garden.objects.get(id=garden_id)
        
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

@login_required
def add_garden(request):
    """ Handles form submission for creating a new plant. """
    if request.method == "POST":
        garden_name = request.POST.get("garden_name")
        if not garden_name:
            garden_name = f"{request.user.username}'s Garden"  # Fallback if no name provided

        # Check if a garden with this name already exists for the user
        if Garden.objects.filter(user=request.user, name=garden_name).exists():
            return render(request, "main/add_garden.html", {"error": "A garden with this name already exists."})

        # Create a new garden
        garden = Garden.objects.create(user=request.user, name=garden_name)
        return redirect("gardens")
    
    return render(request, "main/add_garden.html")


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



@require_POST  # Important: Only allow POST requests
@login_required
def create_garden(request):
    garden_name = request.POST.get('garden_name')
    if garden_name:
        Garden.objects.create(name=garden_name, user=request.user)
        # Redirect back to the garden list (or wherever you want)
        return redirect('gardens')  # Replace 'garden_list' with your URL name
    else:
        return JsonResponse({'error': 'Garden name is required'})


@require_POST
@login_required
def rename_garden(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id, user=request.user) # Ensure user owns garden
    new_name = request.POST.get('garden_name')
    if new_name:
        garden.name = new_name
        garden.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': "New name is required"})


@require_POST  # Or @require_http_methods(['DELETE']) if you use DELETE
@login_required
def delete_garden(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id, user=request.user) # Ensure user owns garden
    garden.delete()
    return JsonResponse({'message': 'success'})