from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

# Garden model (Each user can have multiple gardens)
class Garden(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link garden to a user
    name = models.CharField(max_length=100)  # Garden name

    def __str__(self):
        return f"{self.name} (Owned by {self.user.username})"


# Plant model (Each garden can have multiple plants)
class Plant(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)  # Link to a garden
    name = models.CharField(max_length=100)  # Plant name
    species = models.CharField(max_length=100, blank=True, null=True)
    hardware_id = models.CharField(max_length=100, blank=True, null=True) # Optional species (for DB plants)
    optimal_temperature = models.FloatField(blank=True, null=True)
    optimal_humidity = models.FloatField(blank=True, null=True)
    optimal_soil_moisture = models.FloatField(blank=True, null=True)
    optimal_light = models.FloatField(blank=True, null=True)

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
