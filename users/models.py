from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """自定义用户模型"""
    USER_TYPE_CHOICES = [
        ('buyer', '买家'),
        ('artist', '艺术家'),
        ('merchant', '商家'),
    ]
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='buyer',
        verbose_name='用户类型'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    wechat = models.CharField(max_length=50, blank=True, verbose_name='微信号')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    is_verified = models.BooleanField(default=False, verbose_name='是否认证')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class ArtistProfile(models.Model):
    """艺术家档案"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    artist_name = models.CharField(max_length=100, verbose_name='艺术家名称')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    tags = models.JSONField(default=list, verbose_name='标签')
    is_approved = models.BooleanField(default=False, verbose_name='是否通过审核')
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name='审核通过时间')
    followers_count = models.PositiveIntegerField(default=0, verbose_name='粉丝数')
    works_count = models.PositiveIntegerField(default=0, verbose_name='作品数')
    
    # 资质材料字段
    portfolio_images = models.JSONField(default=list, verbose_name='作品集图片')
    education_background = models.TextField(blank=True, verbose_name='教育背景')
    professional_experience = models.TextField(blank=True, verbose_name='专业经历')
    awards_honors = models.TextField(blank=True, verbose_name='获奖荣誉')
    exhibition_history = models.TextField(blank=True, verbose_name='展览经历')
    identity_document = models.FileField(upload_to='artist_documents/', blank=True, verbose_name='身份证明')
    art_qualification = models.FileField(upload_to='artist_documents/', blank=True, verbose_name='艺术资质证明')
    portfolio_document = models.FileField(upload_to='artist_documents/', blank=True, verbose_name='作品集文档')
    other_documents = models.JSONField(default=list, verbose_name='其他证明材料')
    
    # 审核相关字段
    review_notes = models.TextField(blank=True, verbose_name='审核备注')
    rejection_reason = models.TextField(blank=True, verbose_name='拒绝原因')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    
    class Meta:
        verbose_name = '艺术家档案'
        verbose_name_plural = '艺术家档案'
    
    def __str__(self):
        return self.artist_name


class MerchantProfile(models.Model):
    """商家档案"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_profile')
    company_name = models.CharField(max_length=200, verbose_name='公司名称')
    business_license = models.FileField(upload_to='licenses/', verbose_name='营业执照')
    company_description = models.TextField(blank=True, verbose_name='公司描述')
    is_approved = models.BooleanField(default=False, verbose_name='是否通过审核')
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name='审核通过时间')
    
    class Meta:
        verbose_name = '商家档案'
        verbose_name_plural = '商家档案'
    
    def __str__(self):
        return self.company_name


class BuyerProfile(models.Model):
    """买家档案"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    shipping_addresses = models.JSONField(default=list, verbose_name='收货地址')
    favorite_artists = models.ManyToManyField(ArtistProfile, blank=True, verbose_name='收藏的艺术家')
    
    class Meta:
        verbose_name = '买家档案'
        verbose_name_plural = '买家档案'
    
    def __str__(self):
        return f"{self.user.username} 的买家档案"
