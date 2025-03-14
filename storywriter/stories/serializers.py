from rest_framework import serializers
from .models import Story, Character, StorySettings

class StorySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySettings
        fields = '__all__'

class StorySerializer(serializers.ModelSerializer):
    page_count = serializers.SerializerMethodField()
    settings = StorySettingsSerializer()

    class Meta:
        model = Story
        fields = '__all__'

    def get_page_count(self, obj):
        return obj.get_page_count()

    def create(self, validated_data):
        settings_data = validated_data.pop('settings', None)
        story = Story.objects.create(**validated_data)
        if settings_data:
            StorySettings.objects.create(story=story, **settings_data)
        return story

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
