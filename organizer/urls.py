from django.urls import path
from rest_framework import routers

from .views import NoteViewSet, NoteCreateViewSet, AboutView

router= routers.SimpleRouter()

router.register('api/v1', NoteViewSet)
# router.register('api/about', AboutView)

urlpatterns = router.urls
urlpatterns.append(path('api/about/', AboutView.as_view()))


