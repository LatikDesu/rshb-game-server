import json
from pathlib import Path

from api.models import Equipment, Harvest, Minigame
from django.core.management.base import BaseCommand

current_dir = Path(__file__).resolve().parent
equipment_data_file = current_dir / "data/equipment_data.json"
harvest_data_file = current_dir / "data/harvest_data.json"
minigame_data_file = current_dir / "data/minigame_data.json"


class Command(BaseCommand):
    help = "Load common data from JSON file"

    def handle(self, *args, **options):
        with open(equipment_data_file, "r") as file:
            data = json.load(file)

        for item in data:
            equipment, created = Equipment.objects.get_or_create(
                name=item["name"], defaults={"description": item["description"]}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created Equipment: {equipment.name}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Equipment already exists: {equipment.name}")
                )

        with open(harvest_data_file, "r") as file:
            data = json.load(file)

        for item in data:
            harvest, created = Harvest.objects.get_or_create(
                name=item["name"], defaults={"description": item["description"]}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created Harvest: {harvest.name}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Harvest already exists: {harvest.name}")
                )

        with open(minigame_data_file, "r") as file:
            data = json.load(file)

        for item in data:
            game, created = Minigame.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "achievement": item["achievement"],
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Game: {game.name}"))
            else:
                game.description = item["description"]
                game.achievement = item["achievement"]
                game.save()
                self.stdout.write(self.style.SUCCESS(f"Updated Game: {game.name}"))
