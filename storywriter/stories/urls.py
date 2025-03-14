from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoryViewSet, CharacterViewSet, StorySettingsViewSet

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename="stories")
router.register(r'stories/(?P<story_id>\d+)/characters', CharacterViewSet, basename="story-characters")
router.register(r'stories/(?P<story_id>\d+)/settings', StorySettingsViewSet, basename="story-settings")
router.register(r'characters', CharacterViewSet, basename="characters")

urlpatterns = [
    path('', include(router.urls)),
]
