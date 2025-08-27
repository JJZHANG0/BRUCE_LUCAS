from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Banner, Topic, TopicProduct, News, Article, Activity, SearchRecommendation
from .serializers import (
    BannerSerializer, TopicSerializer, TopicProductSerializer, NewsSerializer, NewsListSerializer,
    ArticleSerializer, ArticleListSerializer, ActivitySerializer, SearchRecommendationSerializer
)


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取当前活跃的轮播图"""
        from django.utils import timezone
        now = timezone.now()
        active_banners = self.queryset.filter(
            start_time__lte=now,
            end_time__gte=now
        ).order_by('sort_order')
        serializer = self.get_serializer(active_banners, many=True)
        return Response(serializer.data)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐专题"""
        featured_topics = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_topics, many=True)
        return Response(serializer.data)


class TopicProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TopicProduct.objects.all()
    serializer_class = TopicProductSerializer
    permission_classes = [permissions.AllowAny]


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'summary']
    ordering_fields = ['published_at', 'views_count', 'created_at']
    ordering = ['-published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsSerializer
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """增加浏览量"""
        news = self.get_object()
        news.views_count += 1
        news.save()
        return Response({'message': '浏览量增加成功'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐新闻"""
        featured_news = self.queryset.filter(is_featured=True)[:5]
        serializer = NewsListSerializer(featured_news, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按类型获取新闻"""
        news_type = request.query_params.get('type')
        if news_type:
            news_list = self.queryset.filter(news_type=news_type)
            serializer = NewsListSerializer(news_list, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供新闻类型'}, status=400)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count', 'likes_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        return Article.objects.filter(is_approved=True)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """增加浏览量"""
        article = self.get_object()
        article.views_count += 1
        article.save()
        return Response({'message': '浏览量增加成功'})
    
    @action(detail=True, methods=['post'])
    def increment_likes(self, request, pk=None):
        """增加点赞数"""
        article = self.get_object()
        article.likes_count += 1
        article.save()
        return Response({'message': '点赞成功'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐文章"""
        featured_articles = self.queryset.filter(is_featured=True, is_approved=True)[:5]
        serializer = ArticleListSerializer(featured_articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        """获取我的文章"""
        my_articles = self.queryset.filter(author=request.user)
        serializer = ArticleListSerializer(my_articles, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.filter(is_active=True)
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['start_time']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐活动"""
        featured_activities = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """获取即将开始的活动"""
        from django.utils import timezone
        now = timezone.now()
        upcoming_activities = self.queryset.filter(start_time__gt=now)[:5]
        serializer = self.get_serializer(upcoming_activities, many=True)
        return Response(serializer.data)


class SearchRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SearchRecommendation.objects.filter(is_active=True)
    serializer_class = SearchRecommendationSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ['sort_order']
