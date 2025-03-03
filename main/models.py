from django.db import models
from django.contrib.auth.models import User  

# Garden model (Each user can have multiple gardens)
class Garden(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link garden to a user
    name = models.CharField(max_length=100)  # Garden name

    def __str__(self):
        return f"{self.name} (Owned by {self.user.username})"



class HousePlant(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Light Levels
    preferred_light = models.FloatField()
    min_light = models.FloatField()
    max_light = models.FloatField()

    # Soil Moisture
    preferred_soil_moisture = models.FloatField()
    min_soil_moisture = models.FloatField()
    max_soil_moisture = models.FloatField()

    # Temperature
    preferred_temperature = models.FloatField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()

    # Humidity
    preferred_humidity = models.FloatField()
    min_humidity = models.FloatField()
    max_humidity = models.FloatField()

    def __str__(self):
        return self.name


# Plant model (Each garden can have multiple plants)
class Plant(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)  # Link to a garden
    name = models.CharField(max_length=100)  # Plant name
    houseplant_type = models.ForeignKey(HousePlant, on_delete=models.SET_NULL, null=True, blank=True)
    hardware_id = models.CharField(max_length=100, blank=True, null=True) # Optional species (for DB plants)

    def __str__(self):
        return f"{self.name} in {self.garden.name}"


# Sensor Data model (Each plant has multiple sensor readings)
class SensorData(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)  # Link to a specific plant
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-save time of reading
    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_moisture = models.FloatField()
    light = models.FloatField()

    def __str__(self):
        return f"Data for {self.plant.name} at {self.timestamp}"
