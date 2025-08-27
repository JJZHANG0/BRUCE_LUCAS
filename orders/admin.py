from django.contrib import admin
from .models import Cart, Wishlist, Order, OrderItem, Payment


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__title')
    ordering = ('-added_at',)
    
    readonly_fields = ('total_price',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__title')
    ordering = ('-added_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'final_amount', 'created_at')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('order_number', 'user__username', 'contact_name', 'contact_phone')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('order_number', 'user', 'status')}),
        ('金额信息', {'fields': ('total_amount', 'shipping_fee', 'discount_amount', 'final_amount')}),
        ('收货信息', {'fields': ('shipping_address', 'contact_phone', 'contact_name', 'notes')}),
        ('支付信息', {'fields': ('payment_method', 'payment_time')}),
        ('物流信息', {'fields': ('shipping_time', 'delivery_time')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('order_number', 'created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'total_price')
    search_fields = ('order__order_number', 'product__title')
    ordering = ('order',)
    
    readonly_fields = ('total_price',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'status', 'payment_time', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {'fields': ('order', 'payment_method', 'amount')}),
        ('交易信息', {'fields': ('transaction_id', 'status', 'payment_time')}),
        ('时间信息', {'fields': ('created_at',)}),
    )
    
    readonly_fields = ('created_at',)
