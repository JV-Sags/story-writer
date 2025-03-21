from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from stories.models import Story, Character, StorySettings, StorySetting, Item
from stories.serializers import StorySerializer, CharacterSerializer, StorySettingsSerializer, StorySettingSerializer, ItemSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]  # Requires authentication

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

class StorySettingsViewSet(viewsets.ModelViewSet):
    queryset = StorySettings.objects.all()
    serializer_class = StorySettingsSerializer
    permission_classes = [IsAuthenticated]

class StorySettingViewSet(viewsets.ModelViewSet):
    queryset = StorySetting.objects.all()
    serializer_class = StorySettingSerializer
    permission_classes = [IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
