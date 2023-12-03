from django.contrib import admin

from .models import (
    Equipment,
    Harvest,
    Minigame,
    Player,
    PlayerEquipment,
    PlayerHarvest,
    PlayerMinigame,
)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )


class HarvestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )


class MinigameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "achievement",
    )


class EquipmentInline(admin.TabularInline):
    model = PlayerEquipment
    extra = 0
    readonly = True
    fieldsets = ((None, {"fields": (("equipment_name", "available"),)}),)


class HarvestInline(admin.TabularInline):
    model = PlayerHarvest
    extra = 0
    readonly = True
    fields = (
        "harvest",
        "available",
        "gen_modified",
    )


class MinigameInline(admin.TabularInline):
    model = PlayerMinigame
    extra = 0
    readonly = True
    fields = ("minigame", "available", "complete", "score", "achievement")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "own_money", "own_coins", "top_score", "user_review")
    inlines = [EquipmentInline, MinigameInline]
    save_on_top = True
    save_as = True
    fieldsets = (
        (None, {"fields": (("name", "gender"),)}),
        (None, {"fields": (("own_money", "own_coins", "top_score", "user_review"),)}),
    )


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Harvest, HarvestAdmin)
admin.site.register(Minigame, MinigameAdmin)
