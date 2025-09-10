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
    list_display = ('artist_name', 'user', 'is_approved', 'submitted_at', 'reviewed_at', 'followers_count', 'works_count')
    list_filter = ('is_approved', 'submitted_at', 'reviewed_at')
    search_fields = ('artist_name', 'user__username', 'bio', 'education_background', 'professional_experience')
    readonly_fields = ('submitted_at', 'reviewed_at', 'followers_count', 'works_count')
    
    fieldsets = (
        ('基本信息', {'fields': ('user', 'artist_name', 'bio', 'tags')}),
        ('资质材料', {'fields': ('education_background', 'professional_experience', 'awards_honors', 'exhibition_history')}),
        ('文件材料', {'fields': ('identity_document', 'art_qualification', 'portfolio_document', 'portfolio_images', 'other_documents')}),
        ('审核状态', {'fields': ('is_approved', 'approval_date', 'review_notes', 'rejection_reason', 'submitted_at', 'reviewed_at')}),
        ('统计数据', {'fields': ('followers_count', 'works_count')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        if change and 'is_approved' in form.changed_data:
            from django.utils import timezone
            if obj.is_approved and not obj.reviewed_at:
                obj.reviewed_at = timezone.now()
                obj.approval_date = timezone.now()
        super().save_model(request, obj, form, change)


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
