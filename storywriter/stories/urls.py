from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoryViewSet, CharacterViewSet, StorySettingsViewSet, StorySettingViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'stories', StoryViewSet)
router.register(r'characters', CharacterViewSet)
router.register(r'story-settings', StorySettingsViewSet)
router.register(r'story-setting', StorySettingViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
##Changed
