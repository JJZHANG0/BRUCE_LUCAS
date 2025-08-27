from django.contrib import admin
from .models import Category, PriceRange, SizeRange, Usage, Product, ProductImage, ProductTag, ProductTagRelation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')
    
    fieldsets = (
        ('基本信息', {'fields': ('name', 'parent', 'description')}),
        ('图片', {'fields': ('image',)}),
        ('设置', {'fields': ('sort_order', 'is_active')}),
    )


@admin.register(PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_price', 'max_price')
    search_fields = ('name',)
    ordering = ('min_price',)


@admin.register(SizeRange)
class SizeRangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_size', 'max_size')
    search_fields = ('name',)
    ordering = ('min_size',)


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'price', 'status', 'views_count', 'created_at')
    list_filter = ('status', 'category', 'is_original', 'is_limited', 'created_at')
    search_fields = ('title', 'description', 'artist__artist_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('title', 'description', 'artist', 'category')}),
        ('价格信息', {'fields': ('price', 'original_price')}),
        ('商品属性', {'fields': ('size', 'weight', 'materials', 'techniques', 'year_created')}),
        ('商品设置', {'fields': ('is_original', 'is_limited', 'limited_quantity', 'status')}),
        ('统计数据', {'fields': ('views_count', 'likes_count')}),
    )
    
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'sort_order')
    list_filter = ('is_primary',)
    search_fields = ('product__title', 'alt_text')
    ordering = ('product', 'sort_order')


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(ProductTagRelation)
class ProductTagRelationAdmin(admin.ModelAdmin):
    list_display = ('product', 'tag')
    search_fields = ('product__title', 'tag__name')
