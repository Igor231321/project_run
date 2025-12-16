from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from app_run.models import Run
from app_run.serializers import RunSerializer, UsersSerializer


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UsersSerializer

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get("type", None)

        if user_type == 'coach':
            return qs.filter(is_staff=True)
        elif user_type == 'athlete':
            return  qs.filter(is_staff=False)
        else:
            return qs