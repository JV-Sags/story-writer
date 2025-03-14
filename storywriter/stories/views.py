from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
import random
from .models import Story, Character, StorySettings
from .serializers import StorySerializer, CharacterSerializer, StorySettingsSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

    # 1. Get the number of pages in a story
    @action(detail=True, methods=['get'])
    def pages_count(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        return Response({"story_id": story.id, "title": story.title, "page_count": story.get_page_count()})

    # 2. Get the 5 most recent stories
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_stories = Story.objects.order_by('-created_at')[:5]
        serializer = StorySerializer(recent_stories, many=True)
        return Response(serializer.data)

    # 3. Get the 5 most liked stories
    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_stories = Story.objects.order_by('-likes')[:5]
        serializer = StorySerializer(popular_stories, many=True)
        return Response(serializer.data)

    # 4. Get a random story
    @action(detail=False, methods=['get'])
    def random(self, request):
        story_count = Story.objects.count()
        if story_count == 0:
            return Response({"message": "No stories available"}, status=404)
        random_story = Story.objects.all()[random.randint(0, story_count - 1)]
        serializer = StorySerializer(random_story)
        return Response(serializer.data)

    # 5. Publish a story
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if story.is_published:
            return Response({"message": "Story is already published"}, status=400)
        story.is_published = True
        story.save()
        return Response({"message": "Story published successfully"})

    # 6. Unpublish a story
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if not story.is_published:
            return Response({"message": "Story is already unpublished"}, status=400)
        story.is_published = False
        story.save()
        return Response({"message": "Story unpublished successfully"})

    # 7. Like a story
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.likes += 1
        story.save()
        return Response({"message": "Story liked successfully", "likes": story.likes})

    # 8. Unlike a story
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if story.likes > 0:
            story.likes -= 1
            story.save()
            return Response({"message": "Story unliked successfully", "likes": story.likes})
        return Response({"message": "Story has no likes"}, status=400)

    # 9. Bookmark a story
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.bookmarks += 1
        story.save()
        return Response({"message": "Story bookmarked successfully", "bookmarks": story.bookmarks})

    # 10. Unbookmark a story
    @action(detail=True, methods=['post'])
    def unbookmark(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        if story.bookmarks > 0:
            story.bookmarks -= 1
            story.save()
            return Response({"message": "Story unbookmarked successfully", "bookmarks": story.bookmarks})
        return Response({"message": "Story is not bookmarked"}, status=400)

    # 11. Fetch suggested stories based on likes
    @action(detail=False, methods=['get'])
    def suggested(self, request):
        suggested_stories = Story.objects.filter(is_published=True).order_by('-likes')[:5]
        serializer = StorySerializer(suggested_stories, many=True)
        return Response(serializer.data)

    # 12. Get story statistics
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

    # 13. Assign an existing character to a different story
    @action(detail=True, methods=['post'], url_path='assign-story')
    def assign_story(self, request, pk=None):
        character = get_object_or_404(Character, id=pk)
        new_story_id = request.data.get("story_id")
        if not new_story_id:
            return Response({"error": "story_id is required"}, status=400)
        new_story = get_object_or_404(Story, id=new_story_id)
        character.story = new_story
        character.save()
        return Response({"message": f"Character '{character.name}' assigned to story '{new_story.title}'"})

    # 14. Search for characters
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        characters = Character.objects.filter(Q(name__icontains=query) | Q(background__icontains=query))
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

class StorySettingsViewSet(viewsets.ViewSet):
    # 15. Retrieve settings for a story
    def retrieve(self, request, story_id=None):
        story = get_object_or_404(Story, pk=story_id)
        settings, created = StorySettings.objects.get_or_create(story=story)
        serializer = StorySettingsSerializer(settings)
        return Response(serializer.data)

    # 16. Update story settings
    def update(self, request, story_id=None):
        story = get_object_or_404(Story, pk=story_id)
        settings, created = StorySettings.objects.get_or_create(story=story)
        serializer = StorySettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # 17. Retrieve a Specific Story
    def retrieve(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        serializer = StorySerializer(story)
        return Response(serializer.data)

    # 18. Update a Specific Story
    def update(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        serializer = StorySerializer(story, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 19. Delete a Specific Story
    def destroy(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        story.delete()
        return Response({"message": "Story deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    # 20. List All Stories
    def list(self, request):
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def pages_count(self, request, pk=None):
        story = get_object_or_404(Story, pk=pk)
        return Response({"story_id": story.id, "title": story.title, "page_count": story.get_page_count()})

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

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

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        characters = Character.objects.filter(name__icontains=query) if query else Character.objects.none()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

class StorySettingsViewSet(viewsets.ViewSet):
    def retrieve(self, request, story_id=None):
        story = get_object_or_404(Story, pk=story_id)
        settings, created = StorySettings.objects.get_or_create(story=story)
        serializer = StorySettingsSerializer(settings)
        return Response(serializer.data)

    def update(self, request, story_id=None):
        story = get_object_or_404(Story, pk=story_id)
        settings, created = StorySettings.objects.get_or_create(story=story)
        serializer = StorySettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)   
