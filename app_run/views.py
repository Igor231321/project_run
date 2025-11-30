from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from app_run.models import Run
from app_run.serializers import RunSerializer


@api_view(['GET'])
def company_details(request):
    return Response({
        'company_name': 'Бегуны 30+',
        'slogan': 'Бегаем в любую погоду! От -30 до +30!',
        'contacts': 'Город Задунайск, улица 30 Лет СССР, дом 30'
    })


class RunViewSet(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    queryset = Run.objects.all()
