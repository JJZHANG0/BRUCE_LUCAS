from rest_framework import serializers
from .models import Cart, Wishlist, Order, OrderItem, Payment
from products.models import Product


class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_title', 'product_price', 'product_image', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['total_price', 'added_at']
    
    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return None


class WishlistSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_title', 'product_price', 'product_image', 'added_at']
        read_only_fields = ['added_at']
    
    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'contact_phone', 'contact_name', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # 计算订单总金额
        total_amount = 0
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            product = Product.objects.get(id=product_id)
            total_amount += product.price * quantity
        
        # 创建订单
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            final_amount=total_amount,
            **validated_data
        )
        
        # 创建订单项
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
        
        return order


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at'] 