from rest_framework.viewsets import GenericViewSet
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
    View merged for api/v1
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

        result = notes.data
        for note in result:
            new_qryset = self.get_queryset().filter(author=note['author'])
            note['author'] = new_qryset[0].author.username
        return Response(result)

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
        result['views'] = instance.views + 1
        result['author'] = instance.author.username
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
        if request.user.id != record.author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id != record.author_id:
            if record.public_status:
                if record.title == serializer.data['title'] and \
                    record.note == serializer.data['note'] and \
                    record.note_status == serializer.data['note_status'] and \
                    record.importance_status == serializer.data['importance_status'] and \
                    record.public_status == serializer.data['public_status']:
                    Note.objects.filter(id=record.id).update()
                    return Response(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Note.objects.filter(id=record.id).update()
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
    """
    View for about page
    """
    def get(self, request):
        return HttpResponse(f"<p>current username: {request.user.username}</p><p>server version:</p>")

