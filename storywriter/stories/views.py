from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
import random
from .models import Story, Character, StorySettings, StorySetting, Item
from .serializers import StorySerializer, CharacterSerializer, StorySettingsSerializer, StorySettingSerializer, ItemSerializer

# ViewSet for handling story-related API operations
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

    # Create a new story
    def create(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Retrieve a specific story
    def retrieve(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        serializer = StorySerializer(story)
        return Response(serializer.data)

    # Update a specific story
    def update(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        serializer = StorySerializer(story, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Delete a specific story
    def destroy(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.delete()
        return Response({"message": "Story deleted successfully"}, status=204)

    # List all stories
    def list(self, request):
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

# ViewSet for handling character-related API operations
class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    # Create a new character
    def create(self, request):
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Assign an existing character to a story
    @action(detail=True, methods=['post'])
    def assign_story(self, request, pk=None):
        character = get_object_or_404(Character, id=pk)
        new_story_id = request.data.get("story_id")
        if not new_story_id:
            return Response({"error": "story_id is required"}, status=400)
        new_story = get_object_or_404(Story, id=new_story_id)
        character.story = new_story
        character.save()
        return Response({"message": f"Character '{character.name}' assigned to story '{new_story.title}'"})

    # Search for characters by name or background
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        characters = Character.objects.filter(Q(name__icontains=query) | Q(background__icontains=query))
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

# ViewSet for handling story settings-related API operations
class StorySettingsViewSet(viewsets.ViewSet):
    # Retrieve settings for a specific story
    def retrieve(self, request, story_id=None):
        story = get_object_or_404(Story, pk=story_id)
        settings, created = StorySettings.objects.get_or_create(story=story)
        serializer = StorySettingsSerializer(settings)
        return Response(serializer.data)

    # Update settings for a specific story
    def update(self, request, story_id=None):
        story = get_object_or_404(Story, pk=story_id)
        settings, created = StorySettings.objects.get_or_create(story=story)
        serializer = StorySettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# ViewSet for handling story setting-related API operations (places the story ventures into)
class StorySettingViewSet(viewsets.ModelViewSet):
    queryset = StorySetting.objects.all()
    serializer_class = StorySettingSerializer

    # Create a new story setting
    def create(self, request):
        serializer = StorySettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Retrieve a specific story setting
    def retrieve(self, request, pk=None):
        setting = get_object_or_404(StorySetting, pk=pk)
        serializer = StorySettingSerializer(setting)
        return Response(serializer.data)

    # Update a specific story setting
    def update(self, request, pk=None):
        setting = get_object_or_404(StorySetting, pk=pk)
        serializer = StorySettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Delete a specific story setting
    def destroy(self, request, pk=None):
        setting = get_object_or_404(StorySetting, pk=pk)
        setting.delete()
        return Response({"message": "Setting deleted successfully"}, status=204)

    # List all story settings
    def list(self, request):
        settings = StorySetting.objects.all()
        serializer = StorySettingSerializer(settings, many=True)
        return Response(serializer.data)
    
    # ViewSet for handling item-related API operations
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    # Create a new item
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Retrieve a specific item
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # Update a specific item
    def update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Delete a specific item
    def destroy(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response({"message": "Item deleted successfully"}, status=204)

    # List all items
    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
