from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class Harvest(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урожай"
        verbose_name_plural = "Урожай"


class Minigame(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(blank=False)
    achievement = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"


class Player(models.Model):
    genders = (("Male", "Мужчина"), ("Female", "Женщина"), (None, "Не указан"))

    name = models.CharField(max_length=20, blank=False, unique=True)
    gender = models.CharField(max_length=9, choices=genders, default="Male")
    own_money = models.IntegerField(default=0)
    own_coins = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    top_score = models.IntegerField(default=0)

    user_review = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )

    equipment = models.ManyToManyField(Equipment, through="PlayerEquipment")
    harvest = models.ManyToManyField(Harvest, through="PlayerHarvest")
    minigame = models.ManyToManyField(Minigame, through="PlayerMinigame")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class PlayerEquipment(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=50, blank=False)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"equipment_name: {self.equipment.name}," f"available: {self.available}"


class PlayerHarvest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE)
    harvest_name = models.CharField(max_length=50, blank=False)
    harvest_amount = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    gen_modified = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"harvest_name: {self.harvest.name}, "
            f"harvest_amount: {self.harvest_amount},"
            f"available: {self.available},"
            f"gen_modified: {self.gen_modified}"
        )


class PlayerMinigame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minigame = models.ForeignKey(Minigame, on_delete=models.CASCADE)
    minigame_name = models.CharField(max_length=50, blank=False)
    achievement = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"minigame_name: {self.minigame.name}, "
            f"available: {self.available},"
            f"complete: {self.complete},"
            f"score: {self.score}"
        )
