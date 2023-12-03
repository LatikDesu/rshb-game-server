from django.db.models import Avg
from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Player
from ..serializers import (
    LeaderboardPlayerSerializer,
    PlayerMinigameSerializer,
    PlayerSerializer,
)


class LiderboardView(ReadOnlyModelViewSet):
    serializer_class = LeaderboardPlayerSerializer

    common_minigame_status_codes = {
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

    def get_queryset(self):
        queryset = Player.objects.filter(top_score__gt=0).order_by("-top_score")[:100]
        return queryset

    @extend_schema(
        summary="Получить 100 лучших игроков по очкам",
        tags=["Liderboard"],
        description="""
            Список 100 лучших игроков по очкам.
            Ранжирование по атрибиту top_score в порядке убывания.
            """,
        request=PlayerSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LeaderboardPlayerSerializer,
                description="Ответ получен",
                examples=[
                    OpenApiExample(
                        name="Список лидеров",
                        value={
                            "total_players": 4,
                            "players_with_reviews": 2,
                            "average_review": 5,
                            "leaderboard": [
                                {
                                    "name": "Doom Guy",
                                    "own_coins": 500,
                                    "own_money": 3698,
                                    "user_review": 5,
                                    "top_score": 500,
                                    "achievement": {
                                        "gameFive": {"achievement": False},
                                        "gameThree": {"achievement": False},
                                        "gameOne": {"achievement": True},
                                        "gameTwo": {"achievement": True},
                                        "gameFour": {"achievement": True},
                                    },
                                }
                            ],
                        },
                    )
                ],
            ),
            **common_minigame_status_codes,
        },
    )
    def list(self, request):
        queryset = self.get_queryset()

        total_players = Player.objects.count()
        players_with_reviews = Player.objects.exclude(user_review=None).count()
        average_review = Player.objects.exclude(user_review=None).aggregate(
            Avg("user_review")
        )["user_review__avg"]

        if average_review is None:
            average_review = 0.0

        data = {
            "total_players": total_players,
            "players_with_reviews": players_with_reviews,
            "average_review": average_review,
        }

        serializer = self.serializer_class(queryset, many=True)
        serialized_data = serializer.data

        response_data = {
            "total_players": data["total_players"],
            "players_with_reviews": data["players_with_reviews"],
            "average_review": data["average_review"],
            "leaderboard": serialized_data,
        }

        return Response(response_data)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        pass

    @extend_schema(
        summary="Полученние информации о положении игрока в таблице лидеров",
        tags=["Liderboard"],
        description="""
            Инофрмация о положении игрока в таблице лидеров. Дополнительно список 100 лучших игроков по очкам.

            Параметр запроса:
                id - идентификатор игрока
                GET /api/v1/liderboard/{id}/ranking/
            """,
        request=PlayerSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LeaderboardPlayerSerializer,
                description="Ответ получен",
                examples=[
                    OpenApiExample(
                        name="Список лидеров",
                        value=[
                            {
                                "player_id": 6,
                                "player_name": "Doom Guy 3",
                                "place": 4,
                                "achievement_count": 0,
                                "own_coins": 0,
                                "top_score": 0,
                                "total_players": 4,
                                "user_review": 5,
                                "liderdoard": [
                                    {
                                        "name": "Top_player",
                                        "own_coins": 0,
                                        "own_money": 0,
                                        "top_score": 800,
                                        "user_review": 5,
                                        "achievement": {
                                            "gameOne": {"achievement": False},
                                            "gameTwo": {"achievement": False},
                                            "gameThree": {"achievement": False},
                                            "gameFour": {"achievement": False},
                                            "gameFive": {"achievement": False},
                                        },
                                    }
                                ],
                            }
                        ],
                    )
                ],
            ),
            **common_minigame_status_codes,
        },
    )
    @action(detail=True, methods=["get"], url_path="ranking")
    def get_player_leaderboard(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            raise ValidationError("Player ID должен быть целым числом")

        try:
            player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=404)

        queryset = self.get_queryset()
        serializer_board = self.serializer_class(queryset, many=True)

        players = Player.objects.order_by("-top_score")

        player_rank = list(players).index(player) + 1

        serializer_game = PlayerMinigameSerializer(
            player.playerminigame_set.all(), many=True
        )
        minigame_data = serializer_game.data

        achievement_count = sum(
            1 for game in minigame_data if game.get("achievement", False)
        )

        response_data = {
            "player_id": player.id,
            "player_name": player.name,
            "place": player_rank,
            "achievement_count": achievement_count,
            "own_coins": player.own_coins,
            "top_score": player.top_score,
            "user_review": player.user_review,
            "total_players": players.count(),
            "liderdoard": serializer_board.data,
        }

        return Response(response_data)


class PlayerStatistics(APIView):
    @extend_schema(
        summary="Получить данные по игрокам и оценке",
        tags=["Statistics"],
        description="""
            "activeUsersNum": общее количество зарегистрированных игроков,
            "avgMark": средняя оценка игры
            """,
    )
    def get(self, request) -> Response:
        # Общее количество игроков
        total_players = Player.objects.count()

        # Количество игроков у которых user_review не равно None
        players_with_reviews = Player.objects.exclude(user_review=None).count()

        # Средняя оценка игроков с user_review не равным None
        average_review = Player.objects.exclude(user_review=None).aggregate(
            Avg("user_review")
        )["user_review__avg"]

        if players_with_reviews < 10:
            average_review = 5

        average_review = round(average_review, 1)

        data = {
            "activeUsersNum": total_players,
            "avgMark": average_review,
        }

        return Response(data, status=status.HTTP_200_OK)
