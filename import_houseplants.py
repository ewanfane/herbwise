import csv
from main.models import HousePlant  # Import the model

csv_file_path = "/Users/paulobrien/CS3/Group_Project/herbwise/main/static/main/plant_db.csv"  # Ensure correct file path

def import_houseplants():
    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file, delimiter=";")  # Use semicolon (;) as delimiter

        for row in reader:  # ✅ Correct indentation
            # Convert ranges from "1260-2340" to min/max values
            min_light, max_light = map(float, row["Light Range (lux)"].split("-"))
            min_moisture, max_moisture = map(float, row["Moisture Range (%)"].split("-"))
            min_temperature, max_temperature = map(float, row["Temperature Range (°C)"].split("-"))
            min_humidity, max_humidity = map(float, row["Humidity Range (%)"].split("-"))

            HousePlant.objects.update_or_create(
                name=row["Plant Name"],
                defaults={
                    "preferred_light": float(row["Light (lux)"]),
                    "min_light": min_light,
                    "max_light": max_light,
                    "preferred_soil_moisture": float(row["Moisture (%)"]),
                    "min_soil_moisture": min_moisture,
                    "max_soil_moisture": max_moisture,
                    "preferred_temperature": float(row["Temperature (°C)"]),
                    "min_temperature": min_temperature,
                    "max_temperature": max_temperature,
                    "preferred_humidity": float(row["Humidity (%)"]),
                    "min_humidity": min_humidity,
                    "max_humidity": max_humidity,
                }
            )
    print("✅ Houseplants imported successfully!")

# Run the function
import_houseplants()
