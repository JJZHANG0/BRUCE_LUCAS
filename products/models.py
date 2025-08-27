from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ArtistProfile


class Category(models.Model):
    """商品分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父分类')
    description = models.TextField(blank=True, verbose_name='分类描述')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='分类图片')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class PriceRange(models.Model):
    """价格区间"""
    name = models.CharField(max_length=50, verbose_name='价格区间名称')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最低价格')
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最高价格')
    
    class Meta:
        verbose_name = '价格区间'
        verbose_name_plural = '价格区间'
    
    def __str__(self):
        if self.max_price:
            return f"{self.min_price} - {self.max_price}"
        return f"{self.min_price}+"


class SizeRange(models.Model):
    """尺寸区间"""
    name = models.CharField(max_length=50, verbose_name='尺寸区间名称')
    min_size = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='最小尺寸(cm³)')
    max_size = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='最大尺寸(cm³)')
    
    class Meta:
        verbose_name = '尺寸区间'
        verbose_name_plural = '尺寸区间'
    
    def __str__(self):
        if self.max_size:
            return f"{self.min_size} - {self.max_size} cm³"
        return f"{self.min_size}+ cm³"


class Usage(models.Model):
    """用途分类"""
    name = models.CharField(max_length=100, verbose_name='用途名称')
    description = models.TextField(blank=True, verbose_name='用途描述')
    
    class Meta:
        verbose_name = '用途分类'
        verbose_name_plural = '用途分类'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """商品模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('sold', '已售出'),
        ('archived', '已归档'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='商品标题')
    description = models.TextField(verbose_name='商品描述')
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='products', verbose_name='艺术家')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='原价')
    size = models.CharField(max_length=100, blank=True, verbose_name='尺寸')
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='重量(kg)')
    materials = models.JSONField(default=list, verbose_name='材质')
    techniques = models.JSONField(default=list, verbose_name='技法')
    year_created = models.PositiveIntegerField(null=True, blank=True, verbose_name='创作年份')
    is_original = models.BooleanField(default=True, verbose_name='是否原创')
    is_limited = models.BooleanField(default=False, verbose_name='是否限量')
    limited_quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name='限量数量')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """商品图片"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='商品')
    image = models.ImageField(upload_to='products/', verbose_name='图片')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='图片描述')
    is_primary = models.BooleanField(default=False, verbose_name='是否主图')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        ordering = ['sort_order']
    
    def __str__(self):
        return f"{self.product.title} - {self.alt_text}"


class ProductTag(models.Model):
    """商品标签"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='标签颜色')
    
    class Meta:
        verbose_name = '商品标签'
        verbose_name_plural = '商品标签'
    
    def __str__(self):
        return self.name


class ProductTagRelation(models.Model):
    """商品标签关联"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE, verbose_name='标签')
    
    class Meta:
        verbose_name = '商品标签关联'
        verbose_name_plural = '商品标签关联'
        unique_together = ['product', 'tag']
    
    def __str__(self):
        return f"{self.product.title} - {self.tag.name}"
