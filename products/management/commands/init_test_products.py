from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage, ProductTag
from users.models import User
from decimal import Decimal
import random


class Command(BaseCommand):
    help = '初始化100条测试商品数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化100条测试商品数据...')
        
        # 获取或创建测试用户
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': '测试',
                'last_name': '用户',
                'user_type': 'buyer'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('创建测试用户: testuser/testpass123')
        
        # 获取所有分类
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('没有找到分类数据，请先运行 python manage.py init_categories'))
            return
        
        # 清空现有商品
        Product.objects.all().delete()
        ProductTag.objects.all().delete()
        
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
            {'name': '创新', 'color': '#BB8FCE'},
            {'name': '精品', 'color': '#85C1E9'},
        ]
        
        tags = []
        for tag_data in tags_data:
            tag, created = ProductTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'color': tag_data['color']}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'创建标签: {tag.name}')
        
        # 绘画类商品数据
        painting_products = [
            {'title': '抽象油画《春日印象》', 'price': 1280.00, 'stock': 5},
            {'title': '水彩画《江南水乡》', 'price': 680.00, 'stock': 8},
            {'title': '素描《人物肖像》', 'price': 350.00, 'stock': 12},
            {'title': '丙烯画《现代都市》', 'price': 890.00, 'stock': 6},
            {'title': '版画《山水之间》', 'price': 450.00, 'stock': 15},
            {'title': '插画《童话世界》', 'price': 280.00, 'stock': 20},
            {'title': '数字绘画《未来城市》', 'price': 1200.00, 'stock': 3},
            {'title': '装饰画《自然风光》', 'price': 580.00, 'stock': 10},
            {'title': '海报《电影经典》', 'price': 120.00, 'stock': 50},
            {'title': '漫画《青春故事》', 'price': 180.00, 'stock': 25},
        ]
        
        # 立体艺术/雕刻类商品数据
        sculpture_products = [
            {'title': '青铜雕塑《思考者》', 'price': 3500.00, 'stock': 3},
            {'title': '木雕《龙凤呈祥》', 'price': 2200.00, 'stock': 2},
            {'title': '石雕《观音像》', 'price': 1800.00, 'stock': 4},
            {'title': '泥塑《民间故事》', 'price': 650.00, 'stock': 8},
            {'title': '陶瓷《青花瓷瓶》', 'price': 1200.00, 'stock': 6},
            {'title': '3D打印《现代艺术》', 'price': 800.00, 'stock': 10},
            {'title': '艺术装置《光影互动》', 'price': 2500.00, 'stock': 2},
            {'title': '模型《建筑经典》', 'price': 450.00, 'stock': 15},
        ]
        
        # 潮玩类商品数据
        toy_products = [
            {'title': '盲盒《可爱动物系列》', 'price': 59.00, 'stock': 100},
            {'title': '手办《动漫角色》', 'price': 280.00, 'stock': 30},
            {'title': '拼装模型《机械战士》', 'price': 180.00, 'stock': 40},
            {'title': '涂鸦《街头艺术》', 'price': 150.00, 'stock': 25},
            {'title': '玩具《益智积木》', 'price': 120.00, 'stock': 60},
        ]
        
        # 周边类商品数据
        merchandise_products = [
            {'title': '动漫周边《角色抱枕》', 'price': 88.00, 'stock': 80},
            {'title': '影视周边《电影海报》', 'price': 45.00, 'stock': 120},
            {'title': '游戏周边《游戏手柄》', 'price': 299.00, 'stock': 35},
            {'title': '小说周边《书签套装》', 'price': 25.00, 'stock': 200},
            {'title': '明星周边《签名照片》', 'price': 150.00, 'stock': 50},
            {'title': '二次元《cosplay服装》', 'price': 380.00, 'stock': 20},
        ]
        
        # 手工艺类商品数据
        craft_products = [
            {'title': '刺绣《花鸟图案》', 'price': 680.00, 'stock': 12},
            {'title': '印染《传统纹样》', 'price': 450.00, 'stock': 18},
            {'title': '布艺《手工抱枕》', 'price': 120.00, 'stock': 45},
            {'title': '编织《手工围巾》', 'price': 180.00, 'stock': 30},
            {'title': '首饰《手工项链》', 'price': 280.00, 'stock': 25},
            {'title': '挂件《手工钥匙扣》', 'price': 35.00, 'stock': 80},
        ]
        
        # 非遗艺术类商品数据
        heritage_products = [
            {'title': '民族工艺《传统服饰》', 'price': 1200.00, 'stock': 8},
            {'title': '传统手工艺《剪纸艺术》', 'price': 180.00, 'stock': 35},
            {'title': '古典艺术《书法作品》', 'price': 800.00, 'stock': 15},
            {'title': '传统绘画《工笔画》', 'price': 1500.00, 'stock': 6},
        ]
        
        # 艺术周边类商品数据
        art_accessories = [
            {'title': '贴纸/卡片《艺术系列》', 'price': 25.00, 'stock': 150},
            {'title': '徽章《艺术徽章》', 'price': 15.00, 'stock': 200},
            {'title': '文具《艺术笔记本》', 'price': 45.00, 'stock': 100},
            {'title': '服饰《艺术T恤》', 'price': 120.00, 'stock': 60},
            {'title': '数字艺术《NFT作品》', 'price': 500.00, 'stock': 10},
        ]
        
        # 合并所有商品数据
        all_products_data = []
        all_products_data.extend(painting_products)
        all_products_data.extend(sculpture_products)
        all_products_data.extend(toy_products)
        all_products_data.extend(merchandise_products)
        all_products_data.extend(craft_products)
        all_products_data.extend(heritage_products)
        all_products_data.extend(art_accessories)
        
        # 如果还不够100条，生成更多随机商品
        while len(all_products_data) < 100:
            category = random.choice(categories)
            base_titles = [
                f'{category.name}作品《{random.choice(["春日", "夏日", "秋日", "冬日"])}印象》',
                f'{category.name}创作《{random.choice(["自然", "城市", "人物", "风景"])}之美》',
                f'{category.name}艺术《{random.choice(["传统", "现代", "古典", "前卫"])}风格》',
                f'{category.name}精品《{random.choice(["限量", "珍藏", "典藏", "精选"])}系列》',
            ]
            
            all_products_data.append({
                'title': random.choice(base_titles),
                'price': round(random.uniform(50, 3000), 2),
                'stock': random.randint(1, 50)
            })
        
        # 确保正好100条
        all_products_data = all_products_data[:100]
        
        # 创建商品
        created_products = []
        for i, product_data in enumerate(all_products_data):
            # 随机选择分类
            category = random.choice(categories)
            
            # 随机选择标签（1-3个）
            product_tags = random.sample(tags, random.randint(1, 3))
            
            # 创建商品
            product = Product.objects.create(
                title=product_data['title'],
                description=f"这是{product_data['title']}的详细描述，展现了{category.name}的独特魅力。",
                price=Decimal(str(product_data['price'])),
                category=category,
                stock=product_data['stock'],
                is_active=True
            )
            product.tags.set(product_tags)
            created_products.append(product)
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'已创建 {i + 1}/100 个商品')
        
        # 创建商品图片（模拟）
        for product in created_products:
            ProductImage.objects.create(
                product=product,
                image='products/default.jpg',  # 需要实际的图片文件
                is_primary=True,
                alt_text=f'{product.title} 主图'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'成功创建 {len(created_products)} 个测试商品！')
        )
        self.stdout.write('测试用户: testuser / testpass123')
        self.stdout.write('现在可以使用这些商品来测试购物车功能了')
        
        # 显示一些统计信息
        category_stats = {}
        for product in created_products:
            cat_name = product.category.name
            category_stats[cat_name] = category_stats.get(cat_name, 0) + 1
        
        self.stdout.write('\n=== 分类统计 ===')
        for cat_name, count in sorted(category_stats.items()):
            self.stdout.write(f'{cat_name}: {count} 个商品') 