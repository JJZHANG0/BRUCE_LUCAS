from rest_framework import serializers
from .models import CustomizationRequest, CustomizationTheme, CommercialCooperation, CustomizationQuote, CustomizationProgress


class CustomizationThemeSerializer(serializers.ModelSerializer):
    usage_name = serializers.CharField(source='usage.name', read_only=True)
    
    class Meta:
        model = CustomizationTheme
        fields = '__all__'


class CustomizationRequestSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    
    class Meta:
        model = CustomizationRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CustomizationRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomizationRequest
        fields = ['request_type', 'customization_type', 'title', 'description', 'reference_images', 
                 'budget_range', 'duration_type', 'expected_delivery', 'artist', 'notes']


class CommercialCooperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialCooperation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CustomizationQuoteSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    request_title = serializers.CharField(source='customization_request.title', read_only=True)
    
    class Meta:
        model = CustomizationQuote
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CustomizationProgressSerializer(serializers.ModelSerializer):
    request_title = serializers.CharField(source='customization_request.title', read_only=True)
    
    class Meta:
        model = CustomizationProgress
        fields = '__all__'
        read_only_fields = ['created_at'] 