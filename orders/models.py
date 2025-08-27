from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from products.models import Product


class Cart(models.Model):
    """购物车"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车'
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    """愿望清单"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items', verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        verbose_name = '愿望清单'
        verbose_name_plural = '愿望清单'
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Order(models.Model):
    """订单"""
    STATUS_CHOICES = [
        ('pending_payment', '待付款'),
        ('paid', '已付款'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment', verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='运费')
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='优惠金额')
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最终金额')
    shipping_address = models.JSONField(verbose_name='收货地址')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    contact_name = models.CharField(max_length=100, verbose_name='联系人')
    notes = models.TextField(blank=True, verbose_name='订单备注')
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='支付方式')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    shipping_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    delivery_time = models.DateTimeField(null=True, blank=True, verbose_name='送达时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_number
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"BL{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """订单项"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.PositiveIntegerField(verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    
    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product.title}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Payment(models.Model):
    """支付记录"""
    PAYMENT_METHOD_CHOICES = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行卡'),
        ('other', '其他'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('success', '成功'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='订单')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='支付方式')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='交易号')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='支付状态')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_payment_method_display()}"
