from rest_framework import serializers
from .models import Banner, Topic, TopicProduct, News, Article, Activity, SearchRecommendation


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TopicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicProduct
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'cover_image', 'news_type', 'author', 'views_count', 'published_at']


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['views_count', 'likes_count', 'created_at', 'updated_at']


class ArticleListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author_username', 'cover_image', 'is_approved', 'is_featured', 'views_count', 'likes_count', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class SearchRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchRecommendation
        fields = '__all__' 