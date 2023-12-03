from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Equipment,
    Harvest,
    Minigame,
    Player,
    PlayerEquipment,
    PlayerHarvest,
    PlayerMinigame,
)


@receiver(post_save, sender=Player)
def create_player_equipment(sender, instance, created, **kwargs):
    if created:
        equipment_list = Equipment.objects.all()
        for equipment in equipment_list:
            PlayerEquipment.objects.create(
                player=instance,
                equipment=equipment,
                equipment_name=equipment.name,
                available=False,
            )


@receiver(post_save, sender=Player)
def create_player_harvest(sender, instance, created, **kwargs):
    if created:
        harvest_list = Harvest.objects.all()
        for harvest in harvest_list:
            PlayerHarvest.objects.create(
                player=instance,
                harvest=harvest,
                harvest_name=harvest.name,
                available=False,
            )


@receiver(post_save, sender=Player)
def create_player_minigame(sender, instance, created, **kwargs):
    if created:
        minigame_list = Minigame.objects.all()
        for minigame in minigame_list:
            PlayerMinigame.objects.create(
                player=instance,
                minigame=minigame,
                minigame_name=minigame.name,
                available=False,
            )
