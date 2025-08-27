from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = '初始化商品分类数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化商品分类数据...')
        
        # 清空现有分类
        Category.objects.all().delete()
        
        # 创建主要分类
        categories_data = [
            {
                'name': '绘画',
                'description': '各种绘画作品',
                'sort_order': 1,
                'children': [
                    {'name': '油画', 'description': '油画作品', 'sort_order': 1},
                    {'name': '水彩', 'description': '水彩画作品', 'sort_order': 2},
                    {'name': '素描', 'description': '素描作品', 'sort_order': 3},
                    {'name': '丙烯', 'description': '丙烯画作品', 'sort_order': 4},
                    {'name': '版画', 'description': '版画作品', 'sort_order': 5},
                    {'name': '插画', 'description': '插画作品', 'sort_order': 6},
                    {'name': '漫画', 'description': '漫画作品', 'sort_order': 7},
                    {'name': '数字绘画', 'description': '数字绘画作品', 'sort_order': 8},
                ]
            },
            {
                'name': '立体艺术/雕刻',
                'description': '立体艺术作品和雕刻品',
                'sort_order': 2,
                'children': [
                    {'name': '木雕', 'description': '木雕作品', 'sort_order': 1},
                    {'name': '石雕', 'description': '石雕作品', 'sort_order': 2},
                    {'name': '泥塑', 'description': '泥塑作品', 'sort_order': 3},
                    {'name': '陶瓷', 'description': '陶瓷作品', 'sort_order': 4},
                    {'name': '艺术装置', 'description': '艺术装置作品', 'sort_order': 5},
                    {'name': '3D打印', 'description': '3D打印艺术作品', 'sort_order': 6},
                ]
            },
            {
                'name': '潮玩',
                'description': '潮流玩具和收藏品',
                'sort_order': 3,
                'children': [
                    {'name': '盲盒', 'description': '盲盒玩具', 'sort_order': 1},
                    {'name': '手办', 'description': '手办模型', 'sort_order': 2},
                    {'name': '拼装模型', 'description': '拼装模型玩具', 'sort_order': 3},
                    {'name': '涂鸦', 'description': '涂鸦艺术作品', 'sort_order': 4},
                    {'name': '二次元', 'description': '二次元相关作品', 'sort_order': 5},
                ]
            },
            {
                'name': '周边',
                'description': '各种周边产品',
                'sort_order': 4,
                'children': [
                    {'name': '动漫周边', 'description': '动漫相关周边', 'sort_order': 1},
                    {'name': '影视周边', 'description': '影视相关周边', 'sort_order': 2},
                    {'name': '游戏周边', 'description': '游戏相关周边', 'sort_order': 3},
                    {'name': '小说周边', 'description': '小说相关周边', 'sort_order': 4},
                    {'name': '明星周边', 'description': '明星相关周边', 'sort_order': 5},
                    {'name': '艺术周边', 'description': '艺术相关周边', 'sort_order': 6},
                    {'name': '海报', 'description': '各种海报', 'sort_order': 7},
                    {'name': '贴纸/卡片', 'description': '贴纸和卡片', 'sort_order': 8},
                    {'name': '徽章', 'description': '各种徽章', 'sort_order': 9},
                    {'name': '装饰画', 'description': '装饰画作品', 'sort_order': 10},
                    {'name': '模型', 'description': '各种模型', 'sort_order': 11},
                    {'name': '服饰', 'description': '艺术相关服饰', 'sort_order': 12},
                    {'name': '文具', 'description': '艺术相关文具', 'sort_order': 13},
                    {'name': '玩具', 'description': '艺术相关玩具', 'sort_order': 14},
                    {'name': '数字艺术', 'description': '数字艺术作品', 'sort_order': 15},
                ]
            },
            {
                'name': '手工艺',
                'description': '传统手工艺品',
                'sort_order': 5,
                'children': [
                    {'name': '刺绣', 'description': '刺绣作品', 'sort_order': 1},
                    {'name': '印染', 'description': '印染作品', 'sort_order': 2},
                    {'name': '布艺', 'description': '布艺作品', 'sort_order': 3},
                    {'name': '首饰', 'description': '手工首饰', 'sort_order': 4},
                    {'name': '挂件', 'description': '手工挂件', 'sort_order': 5},
                    {'name': '编织', 'description': '编织作品', 'sort_order': 6},
                ]
            },
            {
                'name': '非遗艺术',
                'description': '非物质文化遗产艺术',
                'sort_order': 6,
                'children': [
                    {'name': '民族工艺', 'description': '民族传统工艺', 'sort_order': 1},
                ]
            },
        ]
        
        # 创建分类
        for cat_data in categories_data:
            children_data = cat_data.pop('children', [])
            parent_category = Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description'],
                sort_order=cat_data['sort_order'],
                is_active=True
            )
            
            # 创建子分类
            for child_data in children_data:
                Category.objects.create(
                    name=child_data['name'],
                    description=child_data['description'],
                    parent=parent_category,
                    sort_order=child_data['sort_order'],
                    is_active=True
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'成功创建 {len(categories_data)} 个主分类和多个子分类')
        ) 