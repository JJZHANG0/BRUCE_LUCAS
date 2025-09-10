from rest_framework import serializers
from .models import Category, PriceRange, SizeRange, Usage, Product, ProductImage, ProductTag


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_children(self, obj):
        children = Category.objects.filter(parent=obj, is_active=True)
        return CategorySerializer(children, many=True).data


class PriceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRange
        fields = '__all__'


class SizeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeRange
        fields = '__all__'


class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = '__all__'


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    tags = ProductTagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'original_price', 'category', 'primary_image', 
                 'views_count', 'likes_count', 'created_at']
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None


class ProductCreateSerializer(serializers.ModelSerializer):
    """作品创建序列化器"""
    materials = serializers.ListField(child=serializers.CharField(), required=False)
    techniques = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'price', 'original_price',
            'size', 'weight', 'materials', 'techniques', 'year_created',
            'is_original', 'is_limited', 'limited_quantity', 'status'
        ]
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("价格必须大于0")
        return value
    
    def validate_original_price(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("原价必须大于0")
        return value 