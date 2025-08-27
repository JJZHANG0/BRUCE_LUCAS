from django.contrib import admin
from .models import CustomizationRequest, CustomizationTheme, CommercialCooperation, CustomizationQuote, CustomizationProgress


@admin.register(CustomizationRequest)
class CustomizationRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'request_type', 'customization_type', 'status', 'expected_delivery', 'created_at')
    list_filter = ('request_type', 'customization_type', 'status', 'duration_type', 'created_at')
    search_fields = ('title', 'user__username', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('user', 'request_type', 'customization_type', 'title', 'description')}),
        ('定制详情', {'fields': ('reference_images', 'budget_range', 'duration_type', 'expected_delivery')}),
        ('状态设置', {'fields': ('status', 'artist', 'notes')}),
    )


@admin.register(CustomizationTheme)
class CustomizationThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'usage', 'is_active')
    list_filter = ('usage', 'is_active')
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('基本信息', {'fields': ('name', 'description', 'usage')}),
        ('状态', {'fields': ('is_active',)}),
    )


@admin.register(CommercialCooperation)
class CommercialCooperationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'cooperation_type', 'status', 'created_at')
    list_filter = ('cooperation_type', 'status', 'created_at')
    search_fields = ('company_name', 'contact_person', 'contact_email', 'project_description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('公司信息', {'fields': ('company_name', 'cooperation_type')}),
        ('联系人信息', {'fields': ('contact_person', 'contact_phone', 'contact_email')}),
        ('项目信息', {'fields': ('project_description', 'budget_range', 'expected_timeline')}),
        ('状态', {'fields': ('status', 'notes')}),
    )


@admin.register(CustomizationQuote)
class CustomizationQuoteAdmin(admin.ModelAdmin):
    list_display = ('customization_request', 'artist', 'price', 'delivery_time', 'status', 'valid_until', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customization_request__title', 'artist__artist_name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('customization_request', 'artist', 'price', 'delivery_time')}),
        ('报价详情', {'fields': ('description', 'terms_conditions')}),
        ('状态设置', {'fields': ('status', 'valid_until')}),
    )


@admin.register(CustomizationProgress)
class CustomizationProgressAdmin(admin.ModelAdmin):
    list_display = ('customization_request', 'phase', 'progress_percentage', 'created_at')
    list_filter = ('phase', 'created_at')
    search_fields = ('customization_request__title', 'title', 'description')
    ordering = ('customization_request', 'created_at')
    
    fieldsets = (
        ('基本信息', {'fields': ('customization_request', 'phase', 'title', 'description')}),
        ('进度信息', {'fields': ('progress_percentage', 'images')}),
    )
