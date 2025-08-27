from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, Wishlist, Order, OrderItem, Payment
from .serializers import (
    CartSerializer, WishlistSerializer, OrderSerializer, OrderCreateSerializer, PaymentSerializer
)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        """添加到购物车"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
            return Response({'error': '请提供商品ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否已在购物车中
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        """更新购物车商品数量"""
        cart_item = self.get_object()
        quantity = request.data.get('quantity')
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': '商品已从购物车移除'})
        
        cart_item.quantity = quantity
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total(self, request):
        """获取购物车总金额"""
        cart_items = self.get_queryset()
        total = sum(item.total_price for item in cart_items)
        return Response({'total': total})


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_to_wishlist(self, request):
        """添加到愿望清单"""
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({'error': '请提供商品ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )
        
        if created:
            serializer = self.get_serializer(wishlist_item)
            return Response(serializer.data)
        else:
            return Response({'message': '商品已在愿望清单中'})


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """按状态获取订单"""
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = self.get_queryset().filter(status=status_filter)
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供订单状态'}, status=400)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
