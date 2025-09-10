#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blendlumina.settings')
django.setup()

from users.models import User, ArtistProfile

def test_artist_registration():
    print("🎨 艺术家注册和审核流程演示")
    print("=" * 50)
    
    # 1. 模拟艺术家注册
    print("\n1️⃣ 模拟艺术家注册申请...")
    
    # 先创建一个测试用户
    try:
        # 删除可能存在的测试用户
        User.objects.filter(username='test_artist').delete()
        
        # 创建用户
        user = User.objects.create_user(
            username='test_artist',
            email='test_artist@example.com',
            password='password123',
            first_name='张',
            last_name='三',
            user_type='artist',
            phone='13800138000'
        )
        print(f"✅ 用户创建成功: {user.username}")
        
        # 创建艺术家档案（待审核状态）
        artist_profile = ArtistProfile.objects.create(
            user=user,
            artist_name='张三艺术家',
            bio='专业油画艺术家，擅长风景画和人物画，从事艺术创作15年',
            tags=['油画', '风景', '人物', '写实'],
            education_background='中央美术学院油画系本科毕业，研究生学历',
            professional_experience='从事油画创作15年，曾在多家知名画廊举办个展，作品被多个艺术机构收藏',
            awards_honors='2019年获得全国油画大赛金奖，2020年获得青年艺术家奖，2021年获得艺术创新奖',
            exhibition_history='2020年北京798艺术区个展《山水情怀》，2021年上海美术馆联展《当代油画》，2022年广州艺术中心个展《人物肖像》',
            portfolio_images=['/media/artist_documents/portfolio/work1.jpg', '/media/artist_documents/portfolio/work2.jpg'],
            other_documents=['/media/artist_documents/other/cert1.pdf'],
            is_approved=False,  # 待审核
            submitted_at='2024-01-01T00:00:00Z'
        )
        print(f"✅ 艺术家档案创建成功: {artist_profile.artist_name}")
        print(f"   状态: {'已审核' if artist_profile.is_approved else '待审核'}")
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return
    
    # 2. 显示待审核的艺术家列表
    print("\n2️⃣ 查看待审核的艺术家列表...")
    pending_artists = ArtistProfile.objects.filter(is_approved=False)
    print(f"📋 待审核艺术家数量: {pending_artists.count()}")
    
    for artist in pending_artists:
        print(f"\n👤 艺术家: {artist.artist_name}")
        print(f"   📧 邮箱: {artist.user.email}")
        print(f"   📱 电话: {artist.user.phone}")
        print(f"   🎓 教育背景: {artist.education_background}")
        print(f"   🏆 获奖荣誉: {artist.awards_honors}")
        print(f"   📅 提交时间: {artist.submitted_at}")
        print(f"   🏷️ 标签: {', '.join(artist.tags)}")
    
    # 3. 模拟管理员审核
    print("\n3️⃣ 模拟管理员审核过程...")
    
    # 审核通过
    print("\n✅ 管理员审核通过...")
    artist_profile.is_approved = True
    artist_profile.approval_date = '2024-01-01T12:00:00Z'
    artist_profile.review_notes = '资质材料齐全，作品质量优秀，同意通过审核'
    artist_profile.reviewed_at = '2024-01-01T12:00:00Z'
    artist_profile.save()
    
    print(f"✅ 审核通过! 艺术家: {artist_profile.artist_name}")
    print(f"   审核时间: {artist_profile.reviewed_at}")
    print(f"   审核备注: {artist_profile.review_notes}")
    
    # 4. 显示审核后的状态
    print("\n4️⃣ 审核后的艺术家状态...")
    updated_artist = ArtistProfile.objects.get(id=artist_profile.id)
    print(f"👤 艺术家: {updated_artist.artist_name}")
    print(f"   状态: {'已审核' if updated_artist.is_approved else '待审核'}")
    print(f"   审核时间: {updated_artist.reviewed_at}")
    print(f"   审核备注: {updated_artist.review_notes}")
    
    # 5. 显示API接口使用示例
    print("\n5️⃣ API接口使用示例...")
    print("\n📡 获取待审核艺术家列表:")
    print("GET /api/artist-profiles/pending_artists/")
    print("Headers: Authorization: Token <admin_token>")
    
    print("\n📡 审核艺术家申请:")
    print("POST /api/artist-profiles/{id}/review_artist/")
    print("Headers: Authorization: Token <admin_token>")
    print("Body: {\"action\": \"approve\", \"review_notes\": \"审核通过\"}")
    
    print("\n🎉 演示完成！")
    print("\n💡 在实际使用中，管理员可以通过以下方式审核:")
    print("   1. 访问 Django Admin 后台")
    print("   2. 使用 API 接口")
    print("   3. 开发专门的管理界面")

if __name__ == '__main__':
    test_artist_registration()
