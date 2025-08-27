from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ArtistProfile
from products.models import Product


class ArtistShop(models.Model):
    """艺术家店铺"""
    artist = models.OneToOneField(ArtistProfile, on_delete=models.CASCADE, related_name='shop', verbose_name='艺术家')
    shop_name = models.CharField(max_length=200, verbose_name='店铺名称')
    shop_description = models.TextField(blank=True, verbose_name='店铺描述')
    shop_logo = models.ImageField(upload_to='shop_logos/', blank=True, verbose_name='店铺logo')
    shop_banner = models.ImageField(upload_to='shop_banners/', blank=True, verbose_name='店铺横幅')
    is_active = models.BooleanField(default=True, verbose_name='是否营业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '艺术家店铺'
        verbose_name_plural = '艺术家店铺'
    
    def __str__(self):
        return self.shop_name


class ArtistPortfolio(models.Model):
    """艺术家作品集"""
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='portfolios', verbose_name='艺术家')
    title = models.CharField(max_length=200, verbose_name='作品集标题')
    description = models.TextField(blank=True, verbose_name='作品集描述')
    cover_image = models.ImageField(upload_to='portfolio_covers/', blank=True, verbose_name='封面图片')
    is_public = models.BooleanField(default=True, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '艺术家作品集'
        verbose_name_plural = '艺术家作品集'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.title}"


class PortfolioItem(models.Model):
    """作品集项目"""
    portfolio = models.ForeignKey(ArtistPortfolio, on_delete=models.CASCADE, related_name='items', verbose_name='作品集')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    class Meta:
        verbose_name = '作品集项目'
        verbose_name_plural = '作品集项目'
        ordering = ['sort_order']
        unique_together = ['portfolio', 'product']
    
    def __str__(self):
        return f"{self.portfolio.title} - {self.product.title}"


class ArtistService(models.Model):
    """艺术家服务"""
    SERVICE_TYPE_CHOICES = [
        ('custom', '定制服务'),
        ('consultation', '咨询服务'),
        ('workshop', '工作坊'),
        ('other', '其他服务'),
    ]
    
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='services', verbose_name='艺术家')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, verbose_name='服务类型')
    title = models.CharField(max_length=200, verbose_name='服务标题')
    description = models.TextField(verbose_name='服务描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='服务价格')
    duration = models.CharField(max_length=100, blank=True, verbose_name='服务时长')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '艺术家服务'
        verbose_name_plural = '艺术家服务'
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.title}"


class CustomerService(models.Model):
    """客服管理"""
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='customer_services', verbose_name='艺术家')
    service_name = models.CharField(max_length=100, verbose_name='客服名称')
    service_type = models.CharField(max_length=50, verbose_name='服务类型')
    contact_info = models.CharField(max_length=200, verbose_name='联系方式')
    is_online = models.BooleanField(default=False, verbose_name='是否在线')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '客服管理'
        verbose_name_plural = '客服管理'
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.service_name}"


class ArtistTransaction(models.Model):
    """艺术家交易记录"""
    TRANSACTION_TYPE_CHOICES = [
        ('sale', '销售'),
        ('refund', '退款'),
        ('commission', '佣金'),
        ('withdrawal', '提现'),
    ]
    
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='transactions', verbose_name='艺术家')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, verbose_name='交易类型')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='交易金额')
    description = models.TextField(verbose_name='交易描述')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联订单')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '艺术家交易记录'
        verbose_name_plural = '艺术家交易记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.get_transaction_type_display()}"


class ArtistWithdrawal(models.Model):
    """艺术家提现申请"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('completed', '已完成'),
    ]
    
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='withdrawals', verbose_name='艺术家')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='提现金额')
    bank_account = models.CharField(max_length=100, verbose_name='银行账户')
    bank_name = models.CharField(max_length=100, verbose_name='银行名称')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    notes = models.TextField(blank=True, verbose_name='备注')
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name='处理时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    
    class Meta:
        verbose_name = '艺术家提现申请'
        verbose_name_plural = '艺术家提现申请'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.amount}"
