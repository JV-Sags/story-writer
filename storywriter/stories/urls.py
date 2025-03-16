from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoryViewSet, CharacterViewSet, StorySettingViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'stories', StoryViewSet)
router.register(r'characters', CharacterViewSet)
router.register(r'story-settings', StorySettingViewSet)
router.register(r'items', ItemViewSet)  # New item API endpoint

urlpatterns = [
    path('api/', include(router.urls)),
]
