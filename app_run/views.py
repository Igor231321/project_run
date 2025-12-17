from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

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
    queryset = Run.objects.select_related("athlete")


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UsersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get("type", None)

        if user_type == 'coach':
            return qs.filter(is_staff=True)
        elif user_type == 'athlete':
            return qs.filter(is_staff=False)
        else:
            return qs


class UserRunStart(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status not in ['init']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = Run.Status.IN_PROGRESS
            run.save()
            return Response({"run_id": run.id, "status": run.status.label}, status=status.HTTP_200_OK)


class UserRunStop(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status not in ['in_progress']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = Run.Status.FINISHED
            run.save()
            return Response({"run_id": run.id, "status": run.status.label}, status=status.HTTP_200_OK)
