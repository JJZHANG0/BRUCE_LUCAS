"""blendlumina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, ArtistProfileViewSet, MerchantProfileViewSet, BuyerProfileViewSet
from products.views import (
    CategoryViewSet, PriceRangeViewSet, SizeRangeViewSet, UsageViewSet,
    ProductViewSet, ProductImageViewSet, ProductTagViewSet
)
from orders.views import CartViewSet, WishlistViewSet, OrderViewSet, PaymentViewSet
from artists.views import (
    ArtistShopViewSet, ArtistPortfolioViewSet, PortfolioItemViewSet, ArtistServiceViewSet,
    CustomerServiceViewSet, ArtistTransactionViewSet, ArtistWithdrawalViewSet
)
from content.views import (
    BannerViewSet, TopicViewSet, TopicProductViewSet, NewsViewSet, ArticleViewSet,
    ActivityViewSet, SearchRecommendationViewSet
)
from customization.views import (
    CustomizationThemeViewSet, CustomizationRequestViewSet, CommercialCooperationViewSet,
    CustomizationQuoteViewSet, CustomizationProgressViewSet
)

# 创建路由器
router = DefaultRouter()

# 用户相关路由
router.register(r'users', UserViewSet)
router.register(r'artist-profiles', ArtistProfileViewSet)
router.register(r'merchant-profiles', MerchantProfileViewSet)
router.register(r'buyer-profiles', BuyerProfileViewSet)

# 商品相关路由
router.register(r'categories', CategoryViewSet)
router.register(r'price-ranges', PriceRangeViewSet)
router.register(r'size-ranges', SizeRangeViewSet)
router.register(r'usages', UsageViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-tags', ProductTagViewSet)

# 订单相关路由
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'payments', PaymentViewSet, basename='payment')

# 艺术家相关路由
router.register(r'artist-shops', ArtistShopViewSet)
router.register(r'artist-portfolios', ArtistPortfolioViewSet)
router.register(r'portfolio-items', PortfolioItemViewSet)
router.register(r'artist-services', ArtistServiceViewSet)
router.register(r'customer-services', CustomerServiceViewSet)
router.register(r'artist-transactions', ArtistTransactionViewSet, basename='artist-transaction')
router.register(r'artist-withdrawals', ArtistWithdrawalViewSet, basename='artist-withdrawal')

# 内容相关路由
router.register(r'banners', BannerViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'topic-products', TopicProductViewSet)
router.register(r'news', NewsViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'search-recommendations', SearchRecommendationViewSet)

# 定制服务相关路由
router.register(r'customization-themes', CustomizationThemeViewSet)
router.register(r'customization-requests', CustomizationRequestViewSet, basename='customization-request')
router.register(r'commercial-cooperations', CommercialCooperationViewSet)
router.register(r'customization-quotes', CustomizationQuoteViewSet, basename='customization-quote')
router.register(r'customization-progress', CustomizationProgressViewSet, basename='customization-progress')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
