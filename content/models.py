from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ArtistProfile


class Banner(models.Model):
    """轮播图"""
    BANNER_TYPE_CHOICES = [
        ('artist', '艺术家推荐'),
        ('topic', '专题介绍'),
        ('activity', '活动引流'),
        ('advertisement', '付费广告'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='标题')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='副标题')
    image = models.ImageField(upload_to='banners/', verbose_name='图片')
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPE_CHOICES, verbose_name='轮播图类型')
    link_url = models.URLField(blank=True, verbose_name='链接地址')
    target_blank = models.BooleanField(default=False, verbose_name='新窗口打开')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'
        ordering = ['sort_order', '-created_at']
    
    def __str__(self):
        return self.title


class Topic(models.Model):
    """专题"""
    title = models.CharField(max_length=200, verbose_name='专题标题')
    description = models.TextField(verbose_name='专题描述')
    cover_image = models.ImageField(upload_to='topics/', verbose_name='封面图片')
    banner_image = models.ImageField(upload_to='topic_banners/', blank=True, verbose_name='横幅图片')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '专题'
        verbose_name_plural = '专题'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TopicProduct(models.Model):
    """专题商品关联"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='products', verbose_name='专题')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='商品')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    class Meta:
        verbose_name = '专题商品关联'
        verbose_name_plural = '专题商品关联'
        ordering = ['sort_order']
        unique_together = ['topic', 'product']
    
    def __str__(self):
        return f"{self.topic.title} - {self.product.title}"


class News(models.Model):
    """艺术新闻"""
    NEWS_TYPE_CHOICES = [
        ('art_news', '艺术新闻'),
        ('exhibition', '艺术展'),
        ('culture', '文化展'),
        ('industry', '行业动态'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='新闻标题')
    content = models.TextField(verbose_name='新闻内容')
    summary = models.TextField(blank=True, verbose_name='新闻摘要')
    cover_image = models.ImageField(upload_to='news/', blank=True, verbose_name='封面图片')
    news_type = models.CharField(max_length=20, choices=NEWS_TYPE_CHOICES, verbose_name='新闻类型')
    author = models.CharField(max_length=100, blank=True, verbose_name='作者')
    source = models.CharField(max_length=200, blank=True, verbose_name='来源')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '艺术新闻'
        verbose_name_plural = '艺术新闻'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title


class Article(models.Model):
    """用户文章"""
    title = models.CharField(max_length=20, verbose_name='文章标题')
    content = models.TextField(max_length=1200, verbose_name='文章内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='作者')
    cover_image = models.ImageField(upload_to='articles/', blank=True, verbose_name='封面图片')
    is_approved = models.BooleanField(default=False, verbose_name='是否审核通过')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户文章'
        verbose_name_plural = '用户文章'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Activity(models.Model):
    """活动"""
    ACTIVITY_TYPE_CHOICES = [
        ('heritage', '非遗活动'),
        ('workshop', '工作室特展'),
        ('exhibition', '艺术展览'),
        ('workshop_event', '工作坊活动'),
        ('other', '其他活动'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='活动标题')
    description = models.TextField(verbose_name='活动描述')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, verbose_name='活动类型')
    cover_image = models.ImageField(upload_to='activities/', verbose_name='封面图片')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    location = models.CharField(max_length=200, blank=True, verbose_name='活动地点')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'
        ordering = ['start_time']
    
    def __str__(self):
        return self.title


class SearchRecommendation(models.Model):
    """搜索推荐"""
    RECOMMENDATION_TYPE_CHOICES = [
        ('product', '商品推荐'),
        ('artist', '艺术家推荐'),
        ('keyword', '关键词推荐'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='推荐标题')
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES, verbose_name='推荐类型')
    target_id = models.PositiveIntegerField(verbose_name='目标ID')
    target_type = models.CharField(max_length=50, verbose_name='目标类型')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '搜索推荐'
        verbose_name_plural = '搜索推荐'
        ordering = ['sort_order']
    
    def __str__(self):
        return self.title
