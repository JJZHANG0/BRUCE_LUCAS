from rest_framework import serializers
from .models import ArtistShop, ArtistPortfolio, PortfolioItem, ArtistService, CustomerService, ArtistTransaction, ArtistWithdrawal


class ArtistShopSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    
    class Meta:
        model = ArtistShop
        fields = '__all__'


class ArtistPortfolioSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    
    class Meta:
        model = ArtistPortfolio
        fields = '__all__'


class PortfolioItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    
    class Meta:
        model = PortfolioItem
        fields = '__all__'


class ArtistServiceSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    
    class Meta:
        model = ArtistService
        fields = '__all__'


class CustomerServiceSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    
    class Meta:
        model = CustomerService
        fields = '__all__'


class ArtistTransactionSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = ArtistTransaction
        fields = '__all__'


class ArtistWithdrawalSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    
    class Meta:
        model = ArtistWithdrawal
        fields = '__all__'
        read_only_fields = ['created_at'] 