from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from stories.models import Story, Character, StorySettings, StorySetting, Item
from stories.serializers import StorySerializer, CharacterSerializer, StorySettingsSerializer, StorySettingSerializer, ItemSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class StorySettingsViewSet(viewsets.ModelViewSet):
    queryset = StorySettings.objects.all()
    serializer_class = StorySettingsSerializer

class StorySettingViewSet(viewsets.ModelViewSet):
    queryset = StorySetting.objects.all()
    serializer_class = StorySettingSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
