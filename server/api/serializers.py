from rest_framework.serializers import ModelSerializer

from .models import (
    Equipment,
    Harvest,
    Minigame,
    Player,
    PlayerEquipment,
    PlayerHarvest,
    PlayerMinigame,
)


class EquipmentSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "name", "description")


class HarvestSerializer(ModelSerializer):
    class Meta:
        model = Harvest
        fields = ("id", "name", "description")


class MinigameSerializer(ModelSerializer):
    class Meta:
        model = Minigame
        fields = ("id", "name", "description", "achievement")


class PlayerEquipmentSerializer(ModelSerializer):
    class Meta:
        model = PlayerEquipment
        fields = ("equipment_name", "available")


class PlayerHarvestSerializer(ModelSerializer):
    class Meta:
        model = PlayerHarvest
        fields = ("harvest_name", "harvest_amount", "available", "gen_modified")


class PlayerMinigameSerializer(ModelSerializer):
    class Meta:
        model = PlayerMinigame
        fields = ("minigame_name", "available", "complete", "score", "achievement")


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "gender",
            "own_money",
            "own_coins",
            "user_review",
            "credit",
            "equipment",
            "harvest",
            "minigame",
        )

    equipment = PlayerEquipmentSerializer(
        source="playerequipment_set", many=True, required=False
    )
    harvest = PlayerHarvestSerializer(
        source="playerharvest_set", many=True, required=False
    )
    minigame = PlayerMinigameSerializer(
        source="playerminigame_set", many=True, required=False
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Преобразование equipment в словарь
        equipment_data = {}
        for equipment in data["equipment"]:
            equipment_data[equipment["equipment_name"]] = {
                "available": equipment["available"]
            }

        data["equipment"] = equipment_data

        # Преобразование harvest в словарь
        harvest_data = {}
        for harvest in data["harvest"]:
            harvest_data[harvest["harvest_name"]] = {
                "harvest_amount": harvest["harvest_amount"],
                "available": harvest["available"],
                "gen_modified": harvest["gen_modified"],
            }

        data["harvest"] = harvest_data

        # Преобразование minigame в словарь
        minigame_data = {}
        for minigame in data["minigame"]:
            minigame_data[minigame["minigame_name"]] = {
                "available": minigame["available"],
                "complete": minigame["complete"],
                "score": minigame["score"],
                "achievement": minigame["achievement"],
            }

        data["minigame"] = minigame_data
        return data

    def update(self, instance, validated_data):
        # Обновляем поля Player
        instance.name = validated_data.get("name", instance.name)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.own_money = validated_data.get("own_money", instance.own_money)
        instance.own_coins = validated_data.get("own_coins", instance.own_coins)
        instance.credit = validated_data.get("credit", instance.credit)
        instance.user_review = validated_data.get("user_review", instance.user_review)

        # Проверяем, если own_coins больше текущего top_score, то обновляем top_score
        if validated_data.get("own_coins", instance.own_coins) > instance.top_score:
            instance.top_score = validated_data.get("own_coins", instance.own_coins)

        instance.save()

        equipment_data = validated_data.pop("playerequipment_set", None)
        harvest_data = validated_data.pop("playerharvest_set", None)
        minigame_data = validated_data.pop("playerminigame_set", None)

        instance = super().update(instance, validated_data)

        if equipment_data:
            for equipment_item in equipment_data:
                equipment, created = PlayerEquipment.objects.get_or_create(
                    player=instance, equipment_name=equipment_item["equipment_name"]
                )
                equipment.available = equipment_item["available"]
                equipment.save()

        if harvest_data:
            for harvest_item in harvest_data:
                harvest, created = PlayerHarvest.objects.get_or_create(
                    player=instance, harvest_name=harvest_item["harvest_name"]
                )
                harvest.available = harvest_item["available"]
                harvest.harvest_amount = harvest_item["harvest_amount"]
                harvest.gen_modified = harvest_item["gen_modified"]
                harvest.harvest_name = harvest_item["harvest_name"]
                harvest.save()

        if minigame_data:
            for minigame_item in minigame_data:
                minigame, created = PlayerMinigame.objects.get_or_create(
                    player=instance, minigame_name=minigame_item["minigame_name"]
                )
                minigame.available = minigame_item["available"]
                minigame.complete = minigame_item["complete"]
                minigame.score = minigame_item["score"]
                minigame.minigame_name = minigame_item["minigame_name"]
                minigame.achievement = minigame_item["achievement"]
                minigame.save()

        return instance


class LeaderboardPlayerSerializer(ModelSerializer):
    achievement = PlayerMinigameSerializer(
        source="playerminigame_set", many=True, required=False, read_only=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        achievement_data = {
            minigame["minigame_name"]: {"achievement": minigame["achievement"]}
            for minigame in data["achievement"]
        }

        data["achievement"] = achievement_data
        return data

    class Meta:
        model = Player
        fields = (
            "name",
            "own_coins",
            "own_money",
            "user_review",
            "achievement",
            "top_score",
        )
