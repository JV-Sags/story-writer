from django.db import models

class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)  # Track bookmarks
    created_at = models.DateTimeField(auto_now_add=True)


class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    story = models.ForeignKey(Story, related_name='characters', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class StorySettings(models.Model):
    story = models.OneToOneField(Story, related_name='settings', on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)
    visibility = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')])
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')])

    def __str__(self):
        return f"Settings for {self.story.title}"

