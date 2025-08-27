from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomizationRequest, CustomizationTheme, CommercialCooperation, CustomizationQuote, CustomizationProgress
from .serializers import (
    CustomizationRequestSerializer, CustomizationRequestCreateSerializer, CustomizationThemeSerializer,
    CommercialCooperationSerializer, CustomizationQuoteSerializer, CustomizationProgressSerializer
)


class CustomizationThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomizationTheme.objects.filter(is_active=True)
    serializer_class = CustomizationThemeSerializer
    permission_classes = [permissions.AllowAny]


class CustomizationRequestViewSet(viewsets.ModelViewSet):
    serializer_class = CustomizationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomizationRequest.objects.all()
        return CustomizationRequest.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomizationRequestCreateSerializer
        return CustomizationRequestSerializer
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """按状态获取定制请求"""
        status_filter = request.query_params.get('status')
        if status_filter:
            requests = self.get_queryset().filter(status=status_filter)
            serializer = self.get_serializer(requests, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供状态参数'}, status=400)


class CommercialCooperationViewSet(viewsets.ModelViewSet):
    queryset = CommercialCooperation.objects.all()
    serializer_class = CommercialCooperationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'contact_person', 'project_description']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新合作状态（仅管理员）"""
        if not request.user.is_staff:
            return Response({'error': '权限不足'}, status=403)
        
        new_status = request.data.get('status')
        if new_status not in ['contacted', 'negotiating', 'agreed', 'rejected']:
            return Response({'error': '无效的状态值'}, status=400)
        
        cooperation = self.get_object()
        cooperation.status = new_status
        cooperation.save()
        return Response({'message': '状态更新成功'})


class CustomizationQuoteViewSet(viewsets.ModelViewSet):
    serializer_class = CustomizationQuoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomizationQuote.objects.all()
        return CustomizationQuote.objects.filter(artist__user=self.request.user)


class CustomizationProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CustomizationProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomizationProgress.objects.all()
        return CustomizationProgress.objects.filter(customization_request__user=self.request.user)
