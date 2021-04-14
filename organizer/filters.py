from django_filters import rest_framework as r_filter

from .models import Note


class NoteFilter(r_filter.FilterSet):
    importance_status = r_filter.BooleanFilter(
        field_name="importance_status"
    )
    public_status = r_filter.BooleanFilter(
        field_name="public_status"
    )
    note_status = r_filter.MultipleChoiceFilter(
        field_name="note_status",
        choices=Note.StatusType.choices
    )
    min_views = r_filter.NumberFilter(field_name="views", lookup_expr='gte')
    max_views = r_filter.NumberFilter(field_name="views", lookup_expr='lte')


    class Meta:
        model = Note
        fields = (
            "importance_status",
            'min_views',
            'max_views',
            'public_status',
            'note_status',
        )