#!/usr/bin/env python
"""
创建20个不同的商品数据
"""
import os
import sys
import django
from decimal import Decimal
import random

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blendlumina.settings')
django.setup()

from users.models import User, ArtistProfile
from products.models import Category, Product, ProductImage, ProductTag, ProductTagRelation


def create_products():
    """创建20个商品"""
    print("开始创建20个商品...")
    
    # 获取分类
    categories = list(Category.objects.all())
    if not categories:
        print("没有找到分类数据，请先运行 python manage.py init_categories")
        return
    
    # 获取或创建艺术家用户
    artist_user, created = User.objects.get_or_create(
        username='artist_test',
        defaults={
            'email': 'artist@example.com',
            'first_name': '测试',
            'last_name': '艺术家',
            'user_type': 'artist',
            'phone': '13800000000',
            'is_verified': True,
            'is_active': True
        }
    )
    if created:
        artist_user.set_password('testpass123')
        artist_user.save()
        print("创建测试艺术家用户: artist_test/testpass123")
    
    # 创建艺术家档案
    artist_profile, created = ArtistProfile.objects.get_or_create(
        user=artist_user,
        defaults={
            'artist_name': '测试艺术家',
            'bio': '这是一个测试艺术家，专注于艺术创作。',
            'tags': ['绘画', '雕塑', '创新'],
            'is_approved': True,
            'followers_count': 100,
            'works_count': 20
        }
    )
    
    # 创建商品标签
    tags_data = [
        {'name': '原创', 'color': '#FF6B6B'},
        {'name': '限量', 'color': '#4ECDC4'},
        {'name': '手工', 'color': '#45B7D1'},
        {'name': '艺术', 'color': '#96CEB4'},
        {'name': '收藏', 'color': '#FFEAA7'},
        {'name': '复古', 'color': '#DDA0DD'},
        {'name': '现代', 'color': '#98D8C8'},
        {'name': '传统', 'color': '#F7DC6F'},
    ]
    
    tags = []
    for tag_data in tags_data:
        tag, created = ProductTag.objects.get_or_create(
            name=tag_data['name'],
            defaults={'color': tag_data['color']}
        )
        tags.append(tag)
        if created:
            print(f"创建标签: {tag.name}")
    
    # 商品数据
    products_data = [
        {
            'title': '抽象油画《春日印象》',
            'description': '这是一幅充满活力的抽象油画，以春天的色彩为主题，展现了艺术家对自然的独特感悟。',
            'price': 1280.00,
            'category_name': '绘画',
            'size': '60x80cm',
            'materials': ['画布', '油画颜料'],
            'techniques': ['手绘', '抽象表现']
        },
        {
            'title': '水彩画《江南水乡》',
            'description': '传统水彩画技法，描绘了江南水乡的美丽景色，色彩清新淡雅。',
            'price': 680.00,
            'category_name': '水彩',
            'size': '40x60cm',
            'materials': ['水彩纸', '水彩颜料'],
            'techniques': ['水彩技法', '写实风格']
        },
        {
            'title': '素描《人物肖像》',
            'description': '精湛的素描技法，展现了人物的神韵和特征，线条流畅有力。',
            'price': 350.00,
            'category_name': '素描',
            'size': '30x40cm',
            'materials': ['素描纸', '铅笔'],
            'techniques': ['素描技法', '人物写生']
        },
        {
            'title': '丙烯画《现代都市》',
            'description': '现代丙烯画作品，展现了都市生活的繁华与活力，色彩鲜明。',
            'price': 890.00,
            'category_name': '丙烯',
            'size': '50x70cm',
            'materials': ['画布', '丙烯颜料'],
            'techniques': ['丙烯技法', '现代风格']
        },
        {
            'title': '版画《山水之间》',
            'description': '传统版画工艺，山水画风格，意境深远，适合收藏。',
            'price': 450.00,
            'category_name': '版画',
            'size': '35x50cm',
            'materials': ['版画纸', '油墨'],
            'techniques': ['版画技法', '传统工艺']
        },
        {
            'title': '插画《童话世界》',
            'description': '充满想象力的插画作品，童话风格，色彩丰富，适合儿童房间装饰。',
            'price': 280.00,
            'category_name': '插画',
            'size': '25x35cm',
            'materials': ['插画纸', '彩色铅笔'],
            'techniques': ['插画技法', '童话风格']
        },
        {
            'title': '数字绘画《未来城市》',
            'description': '现代数字绘画作品，展现了未来城市的科技感和想象力。',
            'price': 1200.00,
            'category_name': '数字绘画',
            'size': '60x80cm',
            'materials': ['数字画布', '数字颜料'],
            'techniques': ['数字绘画', '科幻风格']
        },
        {
            'title': '装饰画《自然风光》',
            'description': '装饰性绘画作品，自然风光主题，适合家居装饰。',
            'price': 580.00,
            'category_name': '装饰画',
            'size': '40x60cm',
            'materials': ['装饰画布', '装饰颜料'],
            'techniques': ['装饰技法', '自然风格']
        },
        {
            'title': '海报《电影经典》',
            'description': '经典电影海报，艺术设计感强，适合收藏和装饰。',
            'price': 120.00,
            'category_name': '海报',
            'size': '50x70cm',
            'materials': ['海报纸', '印刷油墨'],
            'techniques': ['平面设计', '印刷工艺']
        },
        {
            'title': '漫画《青春故事》',
            'description': '青春题材漫画作品，故事情节丰富，画风清新。',
            'price': 180.00,
            'category_name': '漫画',
            'size': '20x30cm',
            'materials': ['漫画纸', '漫画颜料'],
            'techniques': ['漫画技法', '青春风格']
        },
        {
            'title': '青铜雕塑《思考者》',
            'description': '精美的青铜雕塑作品，展现了人类思考的瞬间，工艺精湛。',
            'price': 3500.00,
            'category_name': '木雕',
            'size': '30x40x50cm',
            'materials': ['青铜'],
            'techniques': ['雕塑技法', '金属工艺']
        },
        {
            'title': '木雕《龙凤呈祥》',
            'description': '传统木雕工艺，龙凤图案寓意吉祥如意，适合作为礼品。',
            'price': 2200.00,
            'category_name': '木雕',
            'size': '25x35x45cm',
            'materials': ['红木'],
            'techniques': ['木雕技法', '传统工艺']
        },
        {
            'title': '石雕《观音像》',
            'description': '精美的石雕观音像，工艺精湛，适合收藏和供奉。',
            'price': 1800.00,
            'category_name': '石雕',
            'size': '20x30x40cm',
            'materials': ['青石'],
            'techniques': ['石雕技法', '传统工艺']
        },
        {
            'title': '泥塑《民间故事》',
            'description': '传统泥塑作品，民间故事主题，工艺独特。',
            'price': 650.00,
            'category_name': '泥塑',
            'size': '15x25x35cm',
            'materials': ['陶土'],
            'techniques': ['泥塑技法', '民间工艺']
        },
        {
            'title': '陶瓷《青花瓷瓶》',
            'description': '传统青花瓷器，工艺精湛，适合收藏和装饰。',
            'price': 1200.00,
            'category_name': '陶瓷',
            'size': '高30cm',
            'materials': ['高岭土'],
            'techniques': ['陶瓷技法', '青花工艺']
        },
        {
            'title': '3D打印《现代艺术》',
            'description': '现代3D打印艺术作品，科技感强，造型独特。',
            'price': 800.00,
            'category_name': '3D打印',
            'size': '20x20x20cm',
            'materials': ['PLA材料'],
            'techniques': ['3D打印', '现代工艺']
        },
        {
            'title': '艺术装置《光影互动》',
            'description': '现代艺术装置作品，光影互动效果，适合展览。',
            'price': 2500.00,
            'category_name': '艺术装置',
            'size': '50x50x100cm',
            'materials': ['金属', 'LED灯'],
            'techniques': ['装置艺术', '光影设计']
        },
        {
            'title': '模型《建筑经典》',
            'description': '经典建筑模型，工艺精细，适合收藏和展示。',
            'price': 450.00,
            'category_name': '模型',
            'size': '30x40x50cm',
            'materials': ['木材', '塑料'],
            'techniques': ['模型制作', '建筑工艺']
        },
        {
            'title': '盲盒《可爱动物系列》',
            'description': '可爱的动物系列盲盒，收集乐趣强，适合收藏。',
            'price': 59.00,
            'category_name': '盲盒',
            'size': '8x8x8cm',
            'materials': ['PVC材料'],
            'techniques': ['模型制作', '盲盒设计']
        },
        {
            'title': '手办《动漫角色》',
            'description': '精美的动漫角色手办，工艺精湛，适合收藏。',
            'price': 280.00,
            'category_name': '手办',
            'size': '15x15x25cm',
            'materials': ['树脂'],
            'techniques': ['手办制作', '动漫工艺']
        }
    ]
    
    # 创建商品
    created_products = []
    for i, product_data in enumerate(products_data):
        # 查找分类
        category = None
        for cat in categories:
            if cat.name == product_data['category_name']:
                category = cat
                break
        
        if not category:
            # 如果找不到对应分类，随机选择一个
            category = random.choice(categories)
        
        # 创建商品
        product = Product.objects.create(
            title=product_data['title'],
            description=product_data['description'],
            artist=artist_profile,
            category=category,
            price=Decimal(str(product_data['price'])),
            size=product_data['size'],
            weight=round(random.uniform(0.1, 5.0), 2),
            materials=product_data['materials'],
            techniques=product_data['techniques'],
            year_created=random.randint(2020, 2024),
            is_original=random.choice([True, False]),
            is_limited=random.choice([True, False]),
            limited_quantity=random.randint(1, 100) if random.choice([True, False]) else None,
            status='published',
            views_count=random.randint(0, 1000),
            likes_count=random.randint(0, 100)
        )
        
        # 添加标签
        product_tags = random.sample(tags, random.randint(1, 3))
        for tag in product_tags:
            ProductTagRelation.objects.create(product=product, tag=tag)
        
        # 创建商品图片
        ProductImage.objects.create(
            product=product,
            image='products/default.jpg',
            alt_text=f'{product.title} 主图',
            is_primary=True
        )
        
        created_products.append(product)
        print(f"{i+1:2d}. 创建商品: {product.title} - ¥{product.price}")
    
    print(f"\n成功创建 {len(created_products)} 个商品！")
    print("测试艺术家账号: artist_test / testpass123")
    
    # 显示统计信息
    print(f"\n=== 统计信息 ===")
    print(f"商品总数: {Product.objects.count()}")
    print(f"分类总数: {Category.objects.count()}")
    print(f"标签总数: {ProductTag.objects.count()}")
    print(f"艺术家总数: {ArtistProfile.objects.count()}")


if __name__ == '__main__':
    create_products() 