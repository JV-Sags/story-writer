from rest_framework import serializers
from .models import Story, Character, StorySettings, StorySetting, Item

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

class StorySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySetting
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
##Changed
