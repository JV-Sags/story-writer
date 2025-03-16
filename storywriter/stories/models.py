from django.db import models

# Story model representing a book or novel
class Story(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Character model representing a character in a story
class Character(models.Model):
    name = models.CharField(max_length=255)
    background = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="characters", null=True, blank=True)

    def __str__(self):
        return self.name

# StorySettings model for storing customizable settings of a story
class StorySettings(models.Model):
    story = models.OneToOneField(Story, on_delete=models.CASCADE, related_name="settings")
    genre = models.CharField(max_length=100, null=True, blank=True)
    word_limit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Settings for {self.story.title}"

# StorySetting model for defining locations or settings in the story
class StorySetting(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="story_settings")
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=255)  # Item name
    description = models.TextField()  # Item description
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
