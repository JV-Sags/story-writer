from rest_framework import serializers
from .models import Story, Character, StorySettings, StorySetting
from .models import Item

# Serializer for the Story model
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

# Serializer for the Character model
class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

# Serializer for the StorySettings model
class StorySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySettings
        fields = '__all__'

# Serializer for the StorySetting model (Locations)
class StorySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySetting
        fields = '__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
