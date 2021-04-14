from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, \
    RetrieveModelMixin, \
    CreateModelMixin,\
    UpdateModelMixin, \
    DestroyModelMixin
from django.db.models import Q
from rest_framework.views import APIView
from django.http import HttpResponse

from .serializers import NoteSerializer
from .models import Note
from .filters import NoteFilter


class NoteViewSet(ListModelMixin,
                        RetrieveModelMixin,
                        CreateModelMixin,
                        DestroyModelMixin,
                        UpdateModelMixin,
                        GenericViewSet):
    """
    Readonly view for notes

    List:
    view all

    retrieve:
    view concrete
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = NoteFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(public_status=True)

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            notes = self.get_serializer(self.filter_queryset(self.get_queryset()).filter(Q(public_status=True)
                                                                   | Q(author__username=request.user)),
                                        many=True)
        else:
            notes = self.get_serializer(self.filter_queryset(self.get_queryset()).filter(public_status=True)
                                        , many=True)

        return Response(notes.data)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        serializer: NoteSerializer = self.get_serializer(data=instance.__dict__)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        Note.objects.filter(id=instance.id).update(views=instance.views+1)
        result = serializer.data
        result['views'] = result.get('views', 0) + 1
        return Response(result)

    def create(self, request, *args, **kwargs):
        serializer: NoteSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class NoteCreateViewSet(ListModelMixin,
                        RetrieveModelMixin,
                        CreateModelMixin,
                        DestroyModelMixin,
                        UpdateModelMixin,
                        GenericViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated, )


class AboutView(APIView):
    """"""
    def get(self, request):
        return HttpResponse(f"<p>current username: {request.user.username}</p><p>server version:</p>")

