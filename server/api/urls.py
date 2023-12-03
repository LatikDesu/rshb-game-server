from rest_framework.routers import SimpleRouter

from .views.equipments import EquipmentViewSet
from .views.harvests import HarvestViewSet
from .views.liderboard import LiderboardView
from .views.minigames import MinigameViewSet
from .views.players import PlayerViewSet

router = SimpleRouter()

router.register("api/v1/player", PlayerViewSet, basename="player info")
router.register("api/v1/equipment", EquipmentViewSet, basename="equipment")
router.register("api/v1/harvest", HarvestViewSet, basename="harvest")
router.register("api/v1/minigame", MinigameViewSet, basename="minigame")
router.register("api/v1/liderboard", LiderboardView, basename="liderboard")
