from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ArtistProfile, MerchantProfile, BuyerProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified', 'is_staff', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'phone', 'wechat', 'avatar')}),
        ('用户类型', {'fields': ('user_type', 'is_verified')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('artist_name', 'user', 'is_approved', 'followers_count', 'works_count')
    list_filter = ('is_approved',)
    search_fields = ('artist_name', 'user__username', 'bio')
    
    fieldsets = (
        ('基本信息', {'fields': ('user', 'artist_name', 'bio', 'tags')}),
        ('审核状态', {'fields': ('is_approved', 'approval_date')}),
        ('统计数据', {'fields': ('followers_count', 'works_count')}),
    )


@admin.register(MerchantProfile)
class MerchantProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('company_name', 'user__username', 'company_description')
    
    fieldsets = (
        ('基本信息', {'fields': ('user', 'company_name', 'company_description')}),
        ('营业执照', {'fields': ('business_license',)}),
        ('审核状态', {'fields': ('is_approved', 'approval_date')}),
    )


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'shipping_addresses_count', 'favorite_artists_count')
    search_fields = ('user__username',)
    
    fieldsets = (
        ('基本信息', {'fields': ('user',)}),
        ('收货地址', {'fields': ('shipping_addresses',)}),
        ('收藏', {'fields': ('favorite_artists',)}),
    )
    
    def shipping_addresses_count(self, obj):
        return len(obj.shipping_addresses) if obj.shipping_addresses else 0
    shipping_addresses_count.short_description = '收货地址数量'
    
    def favorite_artists_count(self, obj):
        return obj.favorite_artists.count()
    favorite_artists_count.short_description = '收藏艺术家数量'
