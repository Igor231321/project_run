from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from app_run.models import Run, AthleteInfo
from app_run.serializers import RunSerializer, UsersSerializer


@api_view(['GET'])
def company_details(request):
    return Response({
        'company_name': 'Бегуны 30+',
        'slogan': 'Бегаем в любую погоду! От -30 до +30!',
        'contacts': 'Город Задунайск, улица 30 Лет СССР, дом 30'
    })


class Paginator(PageNumberPagination):
    page_size_query_param = 'size'
    # max_page_size = 5
    # page_size = 5


class RunViewSet(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    queryset = Run.objects.select_related("athlete")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = Paginator


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UsersSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = Paginator

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


class AthleteInfoAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        athlete_data, created = AthleteInfo.objects.get_or_create(user=user)
        return Response({"user_id": athlete_data.user.id, "goals": athlete_data.goals,
                         "weight": athlete_data.weight})

    def put(self, request, user_id):
        data = request.data
        weight = data['weight']
        if not isinstance(int, weight):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if 0 < int(weight) > 900:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        athlete_data, created = AthleteInfo.objects.update_or_create(user=user,
                                                                     defaults={"weight": weight,
                                                                               "goals": data["goals"]})
        return Response({"user_id": athlete_data.user.id, "goals": athlete_data.goals,
                         "weight": athlete_data.weight}, status=status.HTTP_201_CREATED)
