#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blendlumina.settings')
django.setup()

from users.models import ArtistProfile
from django.utils import timezone

def simulate_admin_approval():
    print("🔧 模拟Django Admin后台审核通过...")
    
    # 获取待审核的艺术家
    artist = ArtistProfile.objects.filter(is_approved=False).first()
    
    if not artist:
        print("❌ 没有找到待审核的艺术家")
        return
    
    print(f"👤 找到待审核艺术家: {artist.artist_name}")
    print(f"   提交时间: {artist.submitted_at}")
    print(f"   当前状态: {'已审核' if artist.is_approved else '待审核'}")
    
    # 模拟管理员审核通过
    artist.is_approved = True
    artist.approval_date = timezone.now()
    artist.reviewed_at = timezone.now()
    artist.review_notes = "通过Django Admin后台审核，资质材料齐全，同意通过"
    artist.save()
    
    print(f"✅ 审核通过!")
    print(f"   审核时间: {artist.reviewed_at}")
    print(f"   审核备注: {artist.review_notes}")
    print(f"   当前状态: {'已审核' if artist.is_approved else '待审核'}")
    
    print("\n📋 审核后的艺术家信息:")
    print(f"   艺术家名称: {artist.artist_name}")
    print(f"   用户: {artist.user.username}")
    print(f"   邮箱: {artist.user.email}")
    print(f"   电话: {artist.user.phone}")
    print(f"   简介: {artist.bio}")
    print(f"   标签: {artist.tags}")
    print(f"   审核状态: {'已审核' if artist.is_approved else '待审核'}")
    print(f"   审核时间: {artist.reviewed_at}")
    print(f"   审核备注: {artist.review_notes}")

if __name__ == '__main__':
    simulate_admin_approval()
