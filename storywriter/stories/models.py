from django.db import models

class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="characters")

    def __str__(self):
        return self.name

class StorySettings(models.Model):
    story = models.OneToOneField(Story, on_delete=models.CASCADE, related_name="settings")
    genre = models.CharField(max_length=50)
    visibility = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.story.title}"

class StorySetting(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="locations")
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location} in {self.story.title}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.name

##Changed
