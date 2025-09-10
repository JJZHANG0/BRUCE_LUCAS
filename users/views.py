from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import transaction
from django.utils import timezone
from .models import User, ArtistProfile, MerchantProfile, BuyerProfile
from .serializers import (
    UserSerializer, UserCreateSerializer, ArtistProfileSerializer, 
    MerchantProfileSerializer, BuyerProfileSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '用户注册成功',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register_artist(self, request):
        """艺术家注册接口（需要资质审核）"""
        try:
            with transaction.atomic():
                # 设置用户类型为艺术家
                user_data = request.data.copy()
                user_data['user_type'] = 'artist'
                
                # 创建用户
                user_serializer = UserCreateSerializer(data=user_data)
                if not user_serializer.is_valid():
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                user = user_serializer.save()
                
                # 处理资质材料上传
                portfolio_images = request.FILES.getlist('portfolio_images')
                portfolio_image_urls = []
                for image in portfolio_images:
                    portfolio_image_urls.append(f"/media/artist_documents/portfolio/{image.name}")
                
                other_documents = request.FILES.getlist('other_documents')
                other_document_urls = []
                for doc in other_documents:
                    other_document_urls.append(f"/media/artist_documents/other/{doc.name}")
                
                # 创建艺术家档案（包含资质材料）
                artist_profile_data = {
                    'user': user.id,
                    'artist_name': request.data.get('artist_name', user.username),
                    'bio': request.data.get('bio', ''),
                    'tags': request.data.get('tags', []),
                    'portfolio_images': portfolio_image_urls,
                    'education_background': request.data.get('education_background', ''),
                    'professional_experience': request.data.get('professional_experience', ''),
                    'awards_honors': request.data.get('awards_honors', ''),
                    'exhibition_history': request.data.get('exhibition_history', ''),
                    'other_documents': other_document_urls,
                    'is_approved': False,  # 需要审核
                    'submitted_at': timezone.now()
                }
                
                # 处理文件上传
                if 'identity_document' in request.FILES:
                    artist_profile_data['identity_document'] = request.FILES['identity_document']
                if 'art_qualification' in request.FILES:
                    artist_profile_data['art_qualification'] = request.FILES['art_qualification']
                if 'portfolio_document' in request.FILES:
                    artist_profile_data['portfolio_document'] = request.FILES['portfolio_document']
                
                artist_serializer = ArtistProfileSerializer(data=artist_profile_data)
                if artist_serializer.is_valid():
                    artist_profile = artist_serializer.save()
                    
                    return Response({
                        'message': '艺术家注册申请已提交，等待审核',
                        'user': UserSerializer(user).data,
                        'artist_profile': artist_serializer.data,
                        'review_status': 'pending'
                    }, status=status.HTTP_201_CREATED)
                else:
                    # 如果艺术家档案创建失败，删除用户
                    user.delete()
                    return Response({
                        'error': '艺术家档案创建失败',
                        'details': artist_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': f'艺术家注册失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': '请提供用户名和密码'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user:
            # 创建或获取 token
            token, created = Token.objects.get_or_create(user=user)
            
            # 同时支持 session 和 token 认证
            login(request, user)
            
            return Response({
                'message': '登录成功',
                'user': UserSerializer(user).data,
                'token': token.key,
                'token_type': 'Token'
            })
        else:
            return Response({
                'error': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    @method_decorator(csrf_exempt)
    def logout(self, request):
        logout(request)
        return Response({'message': '退出登录成功'})
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """修改用户信息接口"""
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': '用户信息更新成功',
                    'user': serializer.data
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'更新用户信息失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ArtistProfileViewSet(viewsets.ModelViewSet):
    queryset = ArtistProfile.objects.all()
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def approved(self, request):
        artists = self.queryset.filter(is_approved=True)
        serializer = self.get_serializer(artists, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_profile(self, request):
        """艺术家创建自己的信息接口"""
        try:
            # 检查用户是否已经是艺术家
            if hasattr(request.user, 'artist_profile'):
                return Response({
                    'error': '您已经是艺术家，无法重复创建档案'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查用户类型
            if request.user.user_type != 'artist':
                return Response({
                    'error': '只有艺术家类型的用户才能创建艺术家档案'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 创建艺术家档案
            profile_data = request.data.copy()
            profile_data['user'] = request.user.id
            
            serializer = ArtistProfileSerializer(data=profile_data)
            if serializer.is_valid():
                artist_profile = serializer.save()
                
                return Response({
                    'message': '艺术家档案创建成功',
                    'profile': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': f'创建艺术家档案失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """艺术家更新自己的信息接口"""
        try:
            # 检查用户是否有艺术家档案
            if not hasattr(request.user, 'artist_profile'):
                return Response({
                    'error': '您还没有艺术家档案'
                }, status=status.HTTP_404_NOT_FOUND)
            
            artist_profile = request.user.artist_profile
            serializer = ArtistProfileSerializer(artist_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                return Response({
                    'message': '艺术家档案更新成功',
                    'profile': serializer.data
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': f'更新艺术家档案失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def pending_artists(self, request):
        """获取待审核的艺术家列表（管理员）"""
        if not request.user.is_staff:
            return Response({
                'error': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        
        pending_artists = ArtistProfile.objects.filter(is_approved=False)
        serializer = ArtistProfileSerializer(pending_artists, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def review_artist(self, request, pk=None):
        """审核艺术家申请（管理员）"""
        if not request.user.is_staff:
            return Response({
                'error': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            artist_profile = self.get_object()
            action_type = request.data.get('action')  # 'approve' 或 'reject'
            review_notes = request.data.get('review_notes', '')
            rejection_reason = request.data.get('rejection_reason', '')
            
            if action_type == 'approve':
                artist_profile.is_approved = True
                artist_profile.approval_date = timezone.now()
                artist_profile.review_notes = review_notes
                artist_profile.reviewed_at = timezone.now()
                artist_profile.save()
                
                return Response({
                    'message': '艺术家申请已通过',
                    'artist_profile': ArtistProfileSerializer(artist_profile).data
                })
            elif action_type == 'reject':
                artist_profile.is_approved = False
                artist_profile.rejection_reason = rejection_reason
                artist_profile.review_notes = review_notes
                artist_profile.reviewed_at = timezone.now()
                artist_profile.save()
                
                return Response({
                    'message': '艺术家申请已拒绝',
                    'artist_profile': ArtistProfileSerializer(artist_profile).data
                })
            else:
                return Response({
                    'error': '无效的操作类型'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': f'审核失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MerchantProfileViewSet(viewsets.ModelViewSet):
    queryset = MerchantProfile.objects.all()
    serializer_class = MerchantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
