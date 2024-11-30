from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Artist, Album, Track, Purchased, Category
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, PurchasedSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from datetime import date
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomerProfile

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination

from .serializers import UserDetailSerializer

class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class AlbumListView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumDetailView(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class TrackPagination(PageNumberPagination):
    page_size = 10  # عدد المقاطع في كل صفحة
    page_size_query_param = 'page_size'
    max_page_size = 100

class TrackListView(generics.ListAPIView):
    queryset = Track.objects.all().order_by('-id')  # ترتيب المقاطع حسب آخر إضافة
    serializer_class = TrackSerializer
    pagination_class = TrackPagination

class TrackListByIDView(APIView):
    def get(self, request, album_id):
        tracks = Track.objects.filter(album_id=album_id)

        if not tracks.exists():
            return Response({"detail": "No tracks found for this album."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TrackSerializer(tracks, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrackDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        track = Track.objects.get(pk=pk)
        user = request.user
        is_subscribed = CustomerProfile.objects.get(user=user).is_subscribed

        # التحقق من حالة الاشتراك أو الشراء
        if not is_subscribed:
            return Response({
                "title": track.title,
                "artist": track.artist,
                "lyrics_preview": track.textm[:100] + "...",
                "preview_audio_url": track.audio_file.url,  # للمستخدمين غير المشتركين عرض 20 ثانية فقط
            })
        
        # للمشتركين، عرض كل البيانات
        return Response({
            "title": track.title,
            "artist": track.artist,
            "lyrics": track.textm,
            "audio_url": track.audio_file.url,
        })

class TrackPurchaseView(generics.CreateAPIView):
    queryset = Purchased.objects.all()
    serializer_class = PurchasedSerializer

class TrackCreateView(generics.CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(production=self.request.user) 

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})



def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    track.views += 1  
    track.save()
    return render(request, 'track.html', {'track': track})

def popular_tracks(request):
    tracks = Track.objects.order_by('-views')[:10]  
    return render(request, 'popular_tracks.html', {'tracks': tracks})

def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    album.views += 1  
    album.save()
    return render(request, 'album_detail.html', {'album': album})

def popular_albums(request):
    albums = Album.objects.order_by('-views')[:10]  
    return render(request, 'popular_albums.html', {'albums': albums})


def show_albums(request):
    categories = Category.objects.prefetch_related('album_set').all()  

    
    albums_by_category = {}
    for category in categories:
        albums_list = category.album_set.all() 
        paginator = Paginator(albums_list, 10)  
        page_number = request.GET.get('page') 
        albums = paginator.get_page(page_number)  
        albums_by_category[category] = albums  

    return render(request, 'albums.html', {'albums_by_category': albums_by_category})

def latest_albums_view(request):
    latest_albums = Album.objects.order_by('-id')[:10]
    
    context = {
        'latest_albums': latest_albums,
    }
    return render(request, 'latest_albums.html', context)

def most_viewed_albums_view(request):
    most_viewed_albums = Album.objects.order_by('-views')[:10]
    
    context = {
        'most_viewed_albums': most_viewed_albums,
    }
    return render(request, 'most_viewed_albums.html', context)

@api_view(['GET'])
def latest_albums_api_view(request):
    latest_albums = Album.objects.order_by('-id')[:10]
    serializer = AlbumSerializer(latest_albums, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def most_viewed_albums_api_view(request):
    most_viewed_albums = Album.objects.order_by('-views')[:10]
    serializer = AlbumSerializer(most_viewed_albums, many=True)
    return Response(serializer.data)


def show_tracks(request,pk= None):
    album = Album.objects.filter(pk=pk).first()
    if album is None:
        return render(request, 'home') 
    
    album.views += 1 
    album.save()

    tracks = Track.objects.filter(album=album)
    
    for track in tracks:                
                track.views += 1  
                track.save()

    is_owner_or_subscribed = False
    if request.user.is_authenticated:
        for track in tracks:
            is_owner_or_subscribed = request.user.is_superuser or request.user.groups.filter(name="Owner").exists() or \
                                    Purchased.objects.filter(user=request.user, track=track, end_date__gte=date.today()).exists()
            track.is_owner_or_subscribed = is_owner_or_subscribed

    return render(request, 'tracks.html', {'tracks': tracks})

def latest_tracks_view(request):
    latest_tracks = Track.objects.order_by('-id')[:10]
    
    context = {
        'latest_tracks': latest_tracks,
    }
    return render(request, 'latest_tracks.html', context)

def most_viewed_tracks_view(request):
    most_viewed_tracks = Track.objects.order_by('-views')[:10]
    
    context = {
        'most_viewed_tracks': most_viewed_tracks,
    }
    return render(request, 'most_viewed_tracks.html', context)

def search_view(request):
    query = request.POST.get('q')
    artists = albums = tracks = None

    if query:
       
        artists = Artist.objects.filter(name__icontains=query)
        albums = Album.objects.filter(Q(title__icontains=query) | Q(artist__name__icontains=query))
        tracks = Track.objects.filter(title__icontains=query)

        if tracks:
            for track in tracks:                
                track.views += 1  
                track.save()

    context = {
        'query': query,
        'artists': artists,
        'albums': albums,
        'tracks': tracks,
    }
    return render(request, 'search_results.html', context)

def artist_view(request,pk=None):

    artist = Artist.objects.filter(pk=pk).first()

    albums = Album.objects.filter(artist=artist)

    if not artist:
        return redirect('home')
    
    context = {
        'artist': artist,
        'albums':albums,
    }
    return render(request, 'artist.html', context)

def artists_list_view(request):
    artists = Artist.objects.all().order_by('name')

    paginator = Paginator(artists, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'artists.html', {'page_obj': page_obj})

def subscribe_view(request):
    return render(request, 'subscribe.html')


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

class SearchViewAPI(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get('q', '')
        artists = None
        albums = None
        tracks = None

        if query:
            artists = Artist.objects.filter(name__icontains=query)
            albums = Album.objects.filter(Q(title__icontains=query) | Q(artist__name__icontains=query))
            tracks = Track.objects.filter(title__icontains=query)

        artist_serializer = ArtistSerializer(artists, many=True, context={'request': request})
        album_serializer = AlbumSerializer(albums, many=True, context={'request': request})
        track_serializer = TrackSerializer(tracks, many=True, context={'request': request})

        return Response({
            'artists': artist_serializer.data,
            'albums': album_serializer.data,
            'tracks': track_serializer.data
        })
    

class GetAlbumsByArtistViewAPI(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get('q', '')
        albums = None

        if query:
            albums = Album.objects.filter(Q(artist__name__icontains=query)).distinct()
        else:
            albums = Album.objects.none()

        album_serializer = AlbumSerializer(albums, many=True, context={'request': request})

        return Response({
            'albums': album_serializer.data,
        })

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)