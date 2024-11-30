from rest_framework import serializers
from .models import Artist, Album, Track, Purchased, CustomerProfile
from django.contrib.auth.models import User

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['is_subscribed'] 

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    artist = serializers.CharField(source='album.artist.name')
    album = serializers.CharField(source='album.title')  
    album_cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = '__all__'

    def get_album_cover_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.album.cover_image.url) if obj.album.cover_image else None

class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = '__all__'

class UserDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(source='customerprofile.is_subscribed')

    class Meta:
        model = User
        fields = ['id', 'username', 'is_subscribed']


