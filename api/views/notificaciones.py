from rest_framework.parsers import MultiPartParser 
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser 
from rest_framework.response import Response
from rest_framework import status

from api.models import Notificacion
from api.serializers import NotificacionSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

#class NotificacionView(viewsets.ViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
class NotificacionView(generics.CreateAPIView, generics.ListAPIView):
    parser_classes = (MultiPartParser,)
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    pagination_class = StandardResultsSetPagination
    ordering=['fecha_creacion']

    def create(self, request, *args, **kwargs):
        notificacion = {
            "titulo": request.data.get("titulo"),
            "imagen": request.data.get("imagen")
        }
        serializer = self.get_serializer(data=notificacion)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print('Esta todo bien')
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    """
    def perform_create(self, serializer, request):
        enviador_notificaciones = NotificadorService()
        enviador_notificaciones.send_notificacion(serializer.validated_data)
        super().perform_create(serializer)
       

    @staticmethod
    def _get_users_by_filter(self, request):
        users = User.objects.all()
        print(request.data)
        return users
    """ 