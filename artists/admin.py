from django.contrib import admin
from .models import ArtistShop, ArtistPortfolio, PortfolioItem, ArtistService, CustomerService, ArtistTransaction, ArtistWithdrawal


@admin.register(ArtistShop)
class ArtistShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'artist', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('shop_name', 'artist__artist_name', 'shop_description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('artist', 'shop_name', 'shop_description')}),
        ('图片', {'fields': ('shop_logo', 'shop_banner')}),
        ('状态', {'fields': ('is_active',)}),
    )


@admin.register(ArtistPortfolio)
class ArtistPortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'artist__artist_name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('artist', 'title', 'description')}),
        ('图片', {'fields': ('cover_image',)}),
        ('设置', {'fields': ('is_public',)}),
    )


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'product', 'sort_order')
    list_filter = ('portfolio',)
    search_fields = ('portfolio__title', 'product__title')
    ordering = ('portfolio', 'sort_order')


@admin.register(ArtistService)
class ArtistServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'service_type', 'price', 'is_available', 'created_at')
    list_filter = ('service_type', 'is_available', 'created_at')
    search_fields = ('title', 'artist__artist_name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('artist', 'service_type', 'title', 'description')}),
        ('价格信息', {'fields': ('price', 'duration')}),
        ('状态', {'fields': ('is_available',)}),
    )


@admin.register(CustomerService)
class CustomerServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'artist', 'service_type', 'is_online', 'created_at')
    list_filter = ('service_type', 'is_online', 'created_at')
    search_fields = ('service_name', 'artist__artist_name', 'contact_info')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('artist', 'service_name', 'service_type', 'contact_info')}),
        ('状态', {'fields': ('is_online',)}),
    )


@admin.register(ArtistTransaction)
class ArtistTransactionAdmin(admin.ModelAdmin):
    list_display = ('artist', 'transaction_type', 'amount', 'order', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('artist__artist_name', 'description', 'order__order_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('artist', 'transaction_type', 'amount', 'description')}),
        ('关联订单', {'fields': ('order',)}),
    )


@admin.register(ArtistWithdrawal)
class ArtistWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('artist', 'amount', 'bank_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('artist__artist_name', 'bank_account', 'bank_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('artist', 'amount', 'bank_account', 'bank_name')}),
        ('状态', {'fields': ('status', 'notes', 'processed_at')}),
    )
    
    readonly_fields = ('created_at',)
