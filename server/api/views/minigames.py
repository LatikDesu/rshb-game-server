from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Minigame
from ..serializers import MinigameSerializer


class MinigameViewSet(ReadOnlyModelViewSet):
    queryset = Minigame.objects.all()
    serializer_class = MinigameSerializer

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

    @extend_schema(
        summary="Получение списка всех доступных Мини-игр",
        tags=["Minigame"],
        description="""
        Получение списка всех мини-игр.
        В ответе будет получен список объектов класса "Миниигра".
        """,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MinigameSerializer,
                description="Запрос успешно выполнен",
                examples=[
                    OpenApiExample(
                        "Список миниигр",
                        value={
                            "id": 1,
                            "name": "gameOne",
                            "description": "Действие игры происходит в небольшой лаборатории, где работает Маша. На столе стоит подставка для пробирок и в ней пробирки с разными геномами растений для скрещивания. Напротив стоит Маша и подсказывает какие надо пробирки брать и смешивать.",
                            "achievement": '"Мастер скрещивания": Успешно смешайте все доступные пробирки и создайте все модифицированные растения.',
                        },
                    )
                ],
            ),
            **common_minigame_status_codes,
        },
    )
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        exclude=True,
        summary="Получение Миниигры по идентификатору",
        tags=["Minigame"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MinigameSerializer, description="OK"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=None, description="Объект не найден"
            ),
            **common_minigame_status_codes,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Minigame.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
