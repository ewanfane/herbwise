import csv
import os  # Import the os module
from django.core.management.base import BaseCommand
from django.db import IntegrityError  # Import IntegrityError
from main.models import HousePlant  # Import your HousePlant model

class Command(BaseCommand):
    help = 'Import houseplants from a CSV file'

    def handle(self, *args, **options):
        # Construct the absolute path to the CSV file
        # Get the directory of the current file (import_houseplants.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path relative to the commands directory.
        csv_file_path = os.path.join(current_dir, "plant_db.csv")


        try:  # Add a try-except block to handle file errors
            with open(csv_file_path, "r", encoding='utf-8') as file:  # Specify encoding
                reader = csv.DictReader(file, delimiter=";")

                for row in reader:
                    try:
                        # Convert ranges from "1260-2340" to min/max values
                        min_light, max_light = map(float, row["Light Range (lux)"].split("-"))
                        min_moisture, max_moisture = map(float, row["Moisture Range (%)"].split("-"))
                        min_temperature, max_temperature = map(float, row["Temperature Range (°C)"].split("-"))
                        min_humidity, max_humidity = map(float, row["Humidity Range (%)"].split("-"))

                        HousePlant.objects.update_or_create(
                            name=row["Plant Name"].strip(),  # Remove leading/trailing spaces
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
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Error processing row: {row}.  Error: {e}"))
                        continue  # Skip to the next row
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR(f"Error: A plant with the name '{row['Plant Name']}' already exists."))
                        continue
                    except KeyError as e:
                         self.stdout.write(self.style.ERROR(f"Missing expected column: {e} in row: {row}"))
                         continue
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"An unexpected error occurred processing row {row}: {e}"))
                        continue

            self.stdout.write(self.style.SUCCESS("Houseplants imported successfully!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: CSV file not found at {csv_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))