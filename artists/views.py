from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ArtistShop, ArtistPortfolio, PortfolioItem, ArtistService, CustomerService, ArtistTransaction, ArtistWithdrawal
from .serializers import (
    ArtistShopSerializer, ArtistPortfolioSerializer, PortfolioItemSerializer, ArtistServiceSerializer,
    CustomerServiceSerializer, ArtistTransactionSerializer, ArtistWithdrawalSerializer
)


class ArtistShopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtistShop.objects.filter(is_active=True)
    serializer_class = ArtistShopSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['shop_name', 'shop_description', 'artist__artist_name']


class ArtistPortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtistPortfolio.objects.filter(is_public=True)
    serializer_class = ArtistPortfolioSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'artist__artist_name']


class PortfolioItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = [permissions.AllowAny]


class ArtistServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtistService.objects.filter(is_available=True)
    serializer_class = ArtistServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'artist__artist_name']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']


class CustomerServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerService.objects.all()
    serializer_class = CustomerServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['service_name', 'artist__artist_name']


class ArtistTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArtistTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ArtistTransaction.objects.all()
        return ArtistTransaction.objects.filter(artist__user=self.request.user)


class ArtistWithdrawalViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistWithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ArtistWithdrawal.objects.all()
        return ArtistWithdrawal.objects.filter(artist__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """批准提现申请"""
        if not request.user.is_staff:
            return Response({'error': '权限不足'}, status=403)
        
        withdrawal = self.get_object()
        withdrawal.status = 'approved'
        withdrawal.save()
        return Response({'message': '提现申请已批准'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝提现申请"""
        if not request.user.is_staff:
            return Response({'error': '权限不足'}, status=403)
        
        withdrawal = self.get_object()
        withdrawal.status = 'rejected'
        withdrawal.save()
        return Response({'message': '提现申请已拒绝'})
