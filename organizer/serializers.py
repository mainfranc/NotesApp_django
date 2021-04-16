from rest_framework import serializers

from .models import Note, Comment


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
