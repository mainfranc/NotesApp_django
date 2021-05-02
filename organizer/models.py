from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from django.utils import timezone

from datetime import datetime, timedelta


def _set_date():
    return timezone.now() + timedelta(days=1)


class Note(models.Model):
    class StatusType(models.TextChoices):
        ACTIVE = 'active', gettext_lazy('Активно')
        DELAY = 'delay', gettext_lazy('Отложено')
        DONE = 'done', gettext_lazy('Выполнено')

    title = models.CharField(max_length=255)
    note = models.TextField(max_length=1023, null=True, blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='author')
    comments = models.TextField(max_length=1023, null=True, blank=True)
    note_status = models.CharField(
        max_length=16,
        choices=StatusType.choices,
        default=StatusType.ACTIVE,
        verbose_name='Состояние',
    )
    importance_status = models.BooleanField(default=False)
    public_status = models.BooleanField(default=True)
    task_date_time = models.DateTimeField(default=_set_date)
    views = models.IntegerField(verbose_name="количество просмотров",
                                default=0)

    def __str__(self):
        return f'Note {self.title} by {format(self.task_date_time, "%d/%m/%y %H:%M")} author {self.author.username}'


class Comment(models.Model):
    note_id = models.ForeignKey(Note,
                               on_delete=models.CASCADE,
                               verbose_name='Related Note')
    comment = models.TextField(max_length=255)
    rating = models.IntegerField(default=0)

