from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Equipment
from ..serializers import EquipmentSerializer


class EquipmentViewSet(ReadOnlyModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    common_equipment_status_codes = {
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
        summary='Получение списка всех объектов класса "Оборудование"',
        tags=["Equipment"],
        description="""
        Получение списка всех типов оборудования.
        В ответе будет получен список объектов класса "Оборудование".
        """,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=EquipmentSerializer(many=True),
                description="Ответ получен",
                examples=[
                    OpenApiExample(
                        name="Оборудование",
                        value={
                            "id": 1,
                            "name": "software",
                            "description": "Собирает и обрабатывает информацию о растениях и почве",
                        },
                    )
                ],
            ),
            **common_equipment_status_codes,
        },
    )
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        exclude=True,
        summary='Получение конкретного объекта класса "Оборудование"',
        tags=["Equipment"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=EquipmentSerializer, description="OK"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=None, description="Объект не найден"
            ),
            **common_equipment_status_codes,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
