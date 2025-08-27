from django.contrib import admin
from .models import Banner, Topic, TopicProduct, News, Article, Activity, SearchRecommendation


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'banner_type', 'sort_order', 'is_active', 'start_time', 'end_time', 'created_at')
    list_filter = ('banner_type', 'is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    ordering = ('sort_order', '-created_at')
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'subtitle', 'image', 'banner_type')}),
        ('链接设置', {'fields': ('link_url', 'target_blank')}),
        ('显示设置', {'fields': ('sort_order', 'is_active')}),
        ('时间设置', {'fields': ('start_time', 'end_time')}),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'is_active', 'start_time', 'end_time', 'created_at')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'description')}),
        ('图片', {'fields': ('cover_image', 'banner_image')}),
        ('设置', {'fields': ('is_featured', 'is_active')}),
        ('时间设置', {'fields': ('start_time', 'end_time')}),
    )


@admin.register(TopicProduct)
class TopicProductAdmin(admin.ModelAdmin):
    list_display = ('topic', 'product', 'sort_order')
    list_filter = ('topic',)
    search_fields = ('topic__title', 'product__title')
    ordering = ('topic', 'sort_order')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'news_type', 'author', 'is_featured', 'is_published', 'views_count', 'published_at', 'created_at')
    list_filter = ('news_type', 'is_featured', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'author', 'source')
    ordering = ('-published_at', '-created_at')
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'content', 'summary', 'cover_image')}),
        ('分类信息', {'fields': ('news_type', 'author', 'source')}),
        ('发布设置', {'fields': ('is_featured', 'is_published', 'published_at')}),
        ('统计数据', {'fields': ('views_count',)}),
    )
    
    readonly_fields = ('views_count', 'created_at', 'updated_at')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'is_featured', 'views_count', 'likes_count', 'created_at')
    list_filter = ('is_approved', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'content', 'cover_image')}),
        ('作者信息', {'fields': ('author',)}),
        ('审核设置', {'fields': ('is_approved', 'is_featured')}),
        ('统计数据', {'fields': ('views_count', 'likes_count')}),
    )
    
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'start_time', 'end_time', 'location', 'is_featured', 'is_active', 'created_at')
    list_filter = ('activity_type', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('start_time',)
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'description', 'activity_type', 'cover_image')}),
        ('时间地点', {'fields': ('start_time', 'end_time', 'location')}),
        ('设置', {'fields': ('is_featured', 'is_active')}),
    )


@admin.register(SearchRecommendation)
class SearchRecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recommendation_type', 'target_type', 'target_id', 'sort_order', 'is_active', 'created_at')
    list_filter = ('recommendation_type', 'is_active', 'created_at')
    search_fields = ('title',)
    ordering = ('sort_order',)
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'recommendation_type')}),
        ('目标设置', {'fields': ('target_id', 'target_type')}),
        ('显示设置', {'fields': ('sort_order', 'is_active')}),
    )
