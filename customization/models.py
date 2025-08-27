from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ArtistProfile
from products.models import Category, Usage


class CustomizationRequest(models.Model):
    """定制请求"""
    REQUEST_TYPE_CHOICES = [
        ('personal', '个人定制'),
        ('commercial', '商业定制'),
    ]
    
    CUSTOMIZATION_TYPE_CHOICES = [
        ('painting', '绘画'),
        ('sculpture', '立体艺术/雕刻'),
        ('toy', '潮玩'),
        ('accessory', '周边'),
        ('handicraft', '手工艺'),
        ('heritage', '非遗艺术'),
    ]
    
    DURATION_CHOICES = [
        ('short', '短期订单'),
        ('long', '长期订单'),
        ('multiple', '多次订单'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customization_requests', verbose_name='用户')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, verbose_name='请求类型')
    customization_type = models.CharField(max_length=20, choices=CUSTOMIZATION_TYPE_CHOICES, verbose_name='定制类型')
    title = models.CharField(max_length=200, verbose_name='定制标题')
    description = models.TextField(verbose_name='定制描述')
    reference_images = models.JSONField(default=list, verbose_name='参考图片')
    budget_range = models.CharField(max_length=100, blank=True, verbose_name='预算范围')
    duration_type = models.CharField(max_length=20, choices=DURATION_CHOICES, verbose_name='定制时间')
    expected_delivery = models.DateField(null=True, blank=True, verbose_name='预期交付日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    artist = models.ForeignKey(ArtistProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='指定艺术家')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '定制请求'
        verbose_name_plural = '定制请求'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class CustomizationTheme(models.Model):
    """定制主题"""
    name = models.CharField(max_length=100, verbose_name='主题名称')
    description = models.TextField(blank=True, verbose_name='主题描述')
    usage = models.ForeignKey(Usage, on_delete=models.CASCADE, related_name='customization_themes', verbose_name='用途')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    class Meta:
        verbose_name = '定制主题'
        verbose_name_plural = '定制主题'
    
    def __str__(self):
        return self.name


class CommercialCooperation(models.Model):
    """商业合作"""
    COOPERATION_TYPE_CHOICES = [
        ('institutional', '机构采购'),
        ('heritage', '非遗合作'),
        ('creative', '文创定制'),
        ('design', '艺术设计'),
        ('other', '其他合作'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('contacted', '已联系'),
        ('negotiating', '洽谈中'),
        ('agreed', '已达成'),
        ('rejected', '已拒绝'),
    ]
    
    company_name = models.CharField(max_length=200, verbose_name='公司名称')
    contact_person = models.CharField(max_length=100, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    contact_email = models.EmailField(verbose_name='联系邮箱')
    cooperation_type = models.CharField(max_length=20, choices=COOPERATION_TYPE_CHOICES, verbose_name='合作类型')
    project_description = models.TextField(verbose_name='项目描述')
    budget_range = models.CharField(max_length=100, blank=True, verbose_name='预算范围')
    expected_timeline = models.CharField(max_length=200, blank=True, verbose_name='预期时间线')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '商业合作'
        verbose_name_plural = '商业合作'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.get_cooperation_type_display()}"


class CustomizationQuote(models.Model):
    """定制报价"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('sent', '已发送'),
        ('accepted', '已接受'),
        ('rejected', '已拒绝'),
        ('expired', '已过期'),
    ]
    
    customization_request = models.ForeignKey(CustomizationRequest, on_delete=models.CASCADE, related_name='quotes', verbose_name='定制请求')
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='customization_quotes', verbose_name='艺术家')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='报价')
    delivery_time = models.PositiveIntegerField(verbose_name='交付时间(天)')
    description = models.TextField(verbose_name='报价说明')
    terms_conditions = models.TextField(blank=True, verbose_name='条款条件')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    valid_until = models.DateTimeField(verbose_name='有效期至')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '定制报价'
        verbose_name_plural = '定制报价'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customization_request.title} - {self.artist.artist_name}"


class CustomizationProgress(models.Model):
    """定制进度"""
    PHASE_CHOICES = [
        ('design', '设计阶段'),
        ('production', '制作阶段'),
        ('review', '审核阶段'),
        ('finalization', '完成阶段'),
    ]
    
    customization_request = models.ForeignKey(CustomizationRequest, on_delete=models.CASCADE, related_name='progress_updates', verbose_name='定制请求')
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES, verbose_name='阶段')
    title = models.CharField(max_length=200, verbose_name='进度标题')
    description = models.TextField(verbose_name='进度描述')
    progress_percentage = models.PositiveIntegerField(default=0, verbose_name='进度百分比')
    images = models.JSONField(default=list, verbose_name='进度图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '定制进度'
        verbose_name_plural = '定制进度'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.customization_request.title} - {self.get_phase_display()}"
