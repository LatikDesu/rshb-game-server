from django.shortcuts import get_object_or_404
from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Player
from ..serializers import PlayerSerializer

common_value = {
    "id": 1,
    "name": "Doom Guy",
    "gender": "Male",
    "own_money": 1000,
    "own_coins": 0,
    "credit": 0,
    "user_review": None,
    "equipment": {
        "software": {"available": False},
        "bpla": {"available": False},
        "robot": {"available": False},
    },
    "harvest": {
        "tomatoes": {"harvest_amount": 0, "available": True, "gen_modified": False},
        "peppers": {"harvest_amount": 0, "available": False, "gen_modified": False},
        "strawberries": {
            "harvest_amount": 0,
            "available": False,
            "gen_modified": False,
        },
    },
    "minigame": {
        "gameOne": {"available": True, "complete": False, "score": 0},
        "gameTwo": {"available": False, "complete": False, "score": 0},
        "gameThree": {"available": False, "complete": False, "score": 0},
        "gameFour": {"available": False, "complete": False, "score": 0},
        "gameFive": {"available": False, "complete": False, "score": 0},
    },
}

common_player_status_codes = {
    status.HTTP_200_OK: OpenApiResponse(
        response=PlayerSerializer,
        examples=[
            OpenApiExample(
                "Данные об игроке",
                value=common_value,
            )
        ],
        description="Ответ Получен",
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        response=None, description="Неправильный запрос"
    ),
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=None, description="Пользователь не авторизован"
    ),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        response=None, description="Доступ запрещён"
    ),
    status.HTTP_404_NOT_FOUND: OpenApiResponse(
        response=None, description="Запрашиваемый объект не найден"
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        response=None, description="Внутренняя ошибка сервера"
    ),
}


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        summary='Получение списка всех объектов класса "Игрок"',
        tags=["Player"],
        description="""
        Получение списка всех игроков.
        В ответе будет получен полный список объектов класса "Игрок".
        """,
        request=PlayerSerializer,
        responses=common_player_status_codes,
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Создание объекта класса "Игрок"',
        tags=["Player"],
        description="""
    Создание нового игрока. При создании игрока, вы можете указать следующие поля:

    - `name` (обязательное поле): Имя игрока (максимальная длина 20 символов).
    - `gender`: Пол игрока (выбор из "Male", "Female", по умолчанию 'Male').
    - `own_money`: Количество гринкоинов у игрока (по умолчанию 0).
    - `own_coins`: Количество заработаннывх очков у игрока (по умолчанию 0).
    - `credit`: Размер кредита от банка (по умолчанию 0).
    - `user_review`: Оценка игры пользователем (по умолчанию Null).
    - `equipment`: Связанные записи оборудования игрока (создаются автоматически).
    - `harvest`: Связанные записи урожая игрока (создаются автоматически).
    - `minigame`: Связанные записи мини-игр игрока (создаются автоматически).

    В ответе будет получен объект класса "Игрок".
        """,
        request=PlayerSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=PlayerSerializer,
                examples=[
                    OpenApiExample(
                        name="Данные об игроке",
                        summary="Данные об игроке",
                        value=common_value,
                    )
                ],
                description="Создано",
            ),
            **common_player_status_codes,
        },
        examples=[
            OpenApiExample(
                name="Создание игрока",
                value={"name": "Doom Guy", "gender": "Male"},
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='Получение конкретного объекта класса "Игрок"',
        tags=["Player"],
        description="""
        Получение данных об игроке по его идентификатору.

        Параметр запроса:
            id - идентификатор игрока
            GET /api/v1/players/{id}

        В ответе будет получен объект класса "Игрок".
        """,
        responses=common_player_status_codes,
        examples=[
            OpenApiExample(
                name="Данные об игроке",
                summary="Данные об игроке",
                value=common_value,
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary='Удаление объекта класса "Игрок"',
        tags=["Player"],
        description="""
        Удаление данных об игроке по его идентификатору.

        Параметр запроса:
            id - идентификатор игрока
            DELETE /api/v1/players/{id}

        В ответе будет получен статус-код выполнения.
        """,
        responses={**common_player_status_codes},
    )
    def destroy(self, request, *args, **kwargs):
        instance = instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        exclude=True,
        summary='Полное обновление информации об объекте класса "Игрок"',
        tags=["Player"],
        description="""
            Обновление информации об объекте класса "Игрок".

            Параметр запроса:
                id - идентификатор игрока
                PUT /api/v1/players/{id}

            В теле запроса полная информация об игроке, со всеми полями как в ответе.

            В ответе будет получен статус-код выполненого запроса и объект класса "Игрок".
            """,
        responses=common_player_status_codes,
        examples=[
            OpenApiExample(
                name="Данные об игроке",
                summary="Данные об игроке",
                value=common_value,
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data

        # Преобразование equipment из словаря в список только если есть данные
        equipment_data = data.get("equipment")
        if equipment_data is not None:
            equipment_data = [
                {
                    "equipment_name": equipment_name,
                    "available": equipment_info["available"],
                }
                for equipment_name, equipment_info in equipment_data.items()
                if "available" in equipment_info
            ]
            data["equipment"] = equipment_data

        # Преобразование harvest из словаря в список только если есть данные
        harvest_data = data.get("harvest")
        if harvest_data is not None:
            harvest_data = [
                {
                    "harvest_name": harvest_name,
                    "harvest_amount": harvest_info.get("harvest_amount", 0),
                    "available": harvest_info["available"],
                    "gen_modified": harvest_info.get("gen_modified", False),
                }
                for harvest_name, harvest_info in harvest_data.items()
                if "available" in harvest_info
            ]
            data["harvest"] = harvest_data

        # Преобразование minigame из словаря в список только если есть данные
        minigame_data = data.get("minigame")
        if minigame_data is not None:
            minigame_data = [
                {
                    "minigame_name": minigame_name,
                    "available": minigame_info["available"],
                    "complete": minigame_info.get("complete", False),
                    "score": minigame_info.get("score", 0),
                    "achievement": minigame_info.get("achievement", False),
                }
                for minigame_name, minigame_info in minigame_data.items()
                if "available" in minigame_info
            ]
            data["minigame"] = minigame_data

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary='Добавление/изменение информации об объекте класса "Игрок"',
        tags=["Player"],
        description="""
            Изменение отделных  полей в объекте класса "Игрок".

            Параметр запроса:
                id - идентификатор игрока
                PATCH /api/v1/players/{id}

            В теле запроса информация об игроке, которая должна быть изменена.
            Пример запроса JSON для создания игрока:
            {
                "own_money": 1500,
                "own_coins": 150,
                "credit": 30000,
                "equipment": {
                    "software": {
                        "available": false
                    },
                    "bpla": {
                        "available": false
                    },
                    "robot": {
                        "available": true
                    }
                },
            }

            В ответе будет получен статус-код выполненого запроса и объект класса "Игрок".
            """,
        responses=common_player_status_codes,
        examples=[
            OpenApiExample(
                name="Данные об игроке",
                summary="Данные об игроке",
                value=common_value,
            )
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Сброс данных об игроке на значения по умолчанию",
        tags=["Player"],
        description="""
    Сброс данных об игроке
    В ответе будет получен объект класса "Игрок" с обнулеными данными.
    """,
        request=PlayerSerializer,
        responses=common_player_status_codes,
    )
    @action(detail=True, methods=["get"], url_path="newgame")
    def reset_to_default(self, request, pk=None):
        player = self.get_object()

        # Обновление полей смежной модели PlayerEquipment
        for equipment in player.playerequipment_set.all():
            equipment.available = False
            equipment.save()

        # Обновление полей смежной модели PlayerHarvest
        for harvest in player.playerharvest_set.all():
            harvest.available = False
            harvest.gen_modified = False
            harvest.save()

        # Обновление полей смежной модели PlayerMinigame
        for minigame in player.playerminigame_set.all():
            minigame.available = False
            minigame.complete = False
            minigame.achievement = False
            minigame.score = 0
            minigame.save()

        player.own_money = Player._meta.get_field("own_money").get_default()
        player.own_coins = Player._meta.get_field("own_coins").get_default()
        player.credit = Player._meta.get_field("credit").get_default()
        player.save()

        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)
