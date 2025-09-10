from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Category, PriceRange, SizeRange, Usage, Product, ProductImage, ProductTag, ProductTagRelation
from .serializers import (
    CategorySerializer, PriceRangeSerializer, SizeRangeSerializer, UsageSerializer,
    ProductSerializer, ProductListSerializer, ProductImageSerializer, ProductTagSerializer,
    ProductCreateSerializer
)


# Create your views here.


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        """重写list方法，返回数组格式而不是分页格式"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def root_categories(self, request):
        """获取根分类"""
        root_categories = self.queryset.filter(parent__isnull=True)
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)


class PriceRangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceRange.objects.all()
    serializer_class = PriceRangeSerializer
    permission_classes = [permissions.AllowAny]


class SizeRangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SizeRange.objects.all()
    serializer_class = SizeRangeSerializer
    permission_classes = [permissions.AllowAny]


class UsageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status='published')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'artist', 'status', 'is_original', 'is_limited']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'views_count', 'likes_count']
    ordering = ['-created_at']
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return ProductSerializer
    
    def get_permissions(self):
        """
        根据不同的action设置不同的权限
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """增加浏览量"""
        product = self.get_object()
        product.views_count += 1
        product.save()
        return Response({'message': '浏览量增加成功'})
    
    @action(detail=True, methods=['post'])
    def increment_likes(self, request, pk=None):
        """增加点赞数"""
        product = self.get_object()
        product.likes_count += 1
        product.save()
        return Response({'message': '点赞成功'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐商品"""
        featured_products = self.queryset.filter(is_original=True).order_by('-views_count')[:10]
        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """按分类获取商品"""
        category_id = request.query_params.get('category_id')
        if category_id:
            products = self.queryset.filter(category_id=category_id)
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供分类ID'}, status=400)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_work(self, request):
        """作品上传接口"""
        try:
            with transaction.atomic():
                # 检查用户是否为艺术家
                if not hasattr(request.user, 'artist_profile'):
                    return Response({
                        'error': '只有艺术家才能上传作品'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                # 创建作品
                product_data = request.data.copy()
                product_data['artist'] = request.user.artist_profile.id
                product_data['status'] = 'draft'  # 默认为草稿状态
                
                serializer = ProductCreateSerializer(data=product_data)
                if serializer.is_valid():
                    product = serializer.save()
                    
                    # 处理图片上传
                    images = request.FILES.getlist('images')
                    for i, image in enumerate(images):
                        ProductImage.objects.create(
                            product=product,
                            image=image,
                            alt_text=request.data.get(f'image_alt_{i}', ''),
                            is_primary=(i == 0),  # 第一张图片设为主图
                            sort_order=i
                        )
                    
                    # 处理标签
                    tag_names = request.data.getlist('tags')
                    for tag_name in tag_names:
                        tag, created = ProductTag.objects.get_or_create(name=tag_name)
                        ProductTagRelation.objects.create(product=product, tag=tag)
                    
                    return Response({
                        'message': '作品上传成功',
                        'product': ProductSerializer(product).data
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'作品上传失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [permissions.AllowAny]
