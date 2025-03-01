from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Story
from .serializers import StorySerializer
from rest_framework.decorators import action
from django.db.models import Count
import random
from django.contrib.auth import get_user_model
from django.db.models import Count
from .serializers import CharacterSerializer
from .models import Character
from django.db.models import Q
from .models import StorySettings
from .serializers import StorySerializer, CharacterSerializer, StorySettingsSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a specific story
    def destroy(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.delete()
        return Response({"message": "Story deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

    # Retrieve the 5 most recent stories
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_stories = Story.objects.order_by('-created_at')[:5]
        serializer = StorySerializer(recent_stories, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_stories = Story.objects.order_by('-likes')[:5]
        serializer = StorySerializer(popular_stories, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def random(self, request):
        story_count = Story.objects.count()
        if story_count == 0:
            return Response({"message": "No stories available"}, status=404)
        
        random_index = random.randint(0, story_count - 1)
        random_story = Story.objects.all()[random_index]
        serializer = StorySerializer(random_story)
        return Response(serializer.data)
        # Publish a story, making it publicly visible
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if story.is_published:
            return Response({"message": "Story is already published"}, status=400)
        
        story.is_published = True
        story.save()
        return Response({"message": "Story published successfully"})
        # Unpublish a story, making it private
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if not story.is_published:
            return Response({"message": "Story is already unpublished"}, status=400)
        
        story.is_published = False
        story.save()
        return Response({"message": "Story unpublished successfully"})
        # Like a story to increase engagement
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.likes += 1
        story.save()
        return Response({"message": "Story liked successfully", "likes": story.likes})
        # Unlike a story to remove engagement
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if story.likes > 0:
            story.likes -= 1
            story.save()
            return Response({"message": "Story unliked successfully", "likes": story.likes})
        return 
        # Bookmark a story for future reading
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.bookmarks += 1
        story.save()
        return Response({"message": "Story bookmarked successfully", "bookmarks": story.bookmarks})
        # Remove a story from bookmarks
    @action(detail=True, methods=['post'])
    def unbookmark(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if story.bookmarks > 0:
            story.bookmarks -= 1
            story.save()
            return Response({"message": "Story unbookmarked successfully", "bookmarks": story.bookmarks})
        return Response({"message": "Story is not bookmarked"}, status=400)
        # Get the total number of pages in a specific story
    @action(detail=True, methods=['get'])
    def pages_count(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        word_count = len(story.content.split())  # Count words in content
        pages = max(1, word_count // 500)  # Assume 1 page = 500 words
        return Response({"story_id": story.id, "title": story.title, "word_count": word_count, "pages": pages})
        # Fetch suggested stories based on likes and published status
    @action(detail=False, methods=['get'])
    def suggested(self, request):
        suggested_stories = Story.objects.filter(is_published=True).order_by('-likes')[:5]
        serializer = StorySerializer(suggested_stories, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_stories = Story.objects.count()
        published_stories = Story.objects.filter(is_published=True).count()
        active_authors = Story.objects.values('id').distinct().count()  # Assuming authors are tracked in the future

        return Response({
            "total_stories": total_stories,
            "published_stories": published_stories,
            "active_authors": active_authors
        })
    
    class CharacterViewSet(viewsets.ModelViewSet):
        queryset = Character.objects.all()
        serializer_class = CharacterSerializer
    class CharacterViewSet(viewsets.ViewSet):
    # Retrieve all characters in a specific story
        def list(self, request, story_id=None):
            story = get_object_or_404(Story, id=story_id)
            characters = Character.objects.filter(story=story)
            serializer = CharacterSerializer(characters, many=True)
            return Response(serializer.data)

    # Add a new character to a story
    def create(self, request, story_id=None):
        story = get_object_or_404(Story, id=story_id)
        data = request.data.copy()
        data["story"] = story.id
        serializer = CharacterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Retrieve a specific character
    def retrieve(self, request, story_id=None, character_id=None):
        story = get_object_or_404(Story, id=story_id)
        character = get_object_or_404(Character, id=character_id, story=story)
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    # Update a character's details
    def update(self, request, story_id=None, character_id=None):
        story = get_object_or_404(Story, id=story_id)
        character = get_object_or_404(Character, id=character_id, story=story)
        serializer = CharacterSerializer(character, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Remove a character from a story
    def destroy(self, request, story_id=None, character_id=None):
        story = get_object_or_404(Story, id=story_id)
        character = get_object_or_404(Character, id=character_id, story=story)
        character.delete()
        return Response({"message": "Character deleted successfully"}, status=204)
        # Assign an existing character to a different story
    @action(detail=True, methods=['post'], url_path='assign-story')
    def assign_story(self, request, pk=None):
        character = get_object_or_404(Character, id=pk)
        new_story_id = request.data.get("story_id")

        if not new_story_id:
            return Response({"error": "story_id is required"}, status=400)

        new_story = get_object_or_404(Story, id=new_story_id)
        character.story = new_story
        character.save()

        return Response({
            "message": f"Character '{character.name}' assigned to story '{new_story.title}'",
            "character_id": character.id,
            "new_story_id": new_story.id
        })
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')

        if not query:
            return Response({"error": "Search query parameter 'q' is required"}, status=400)

        characters = Character.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)
    class StorySettingsViewSet(viewsets.ViewSet):
    # Retrieve settings for a specific story
        def retrieve(self, request, pk=None):
            story = get_object_or_404(Story, pk=pk)
            settings = get_object_or_404(StorySettings, story=story)
            serializer = StorySettings(settings)
            return Response(serializer.data)
        # Update story settings (genre, visibility, status)
        # Update story settings (genre, visibility, status)
    def update(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        settings, created = StorySettings.objects.get_or_create(story=story)

        serializer = StorySettings(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

