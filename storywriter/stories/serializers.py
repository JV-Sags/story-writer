from rest_framework import serializers
from .models import Story, Character, StorySettings

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class StorySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySettings
        fields = '__all__'
