from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'note',
            'author',
            'comments',
            'note_status',
            'importance_status',
            'public_status',
            'task_date_time',
            'views'
        ]
        read_only_fields = ('author', 'views', )