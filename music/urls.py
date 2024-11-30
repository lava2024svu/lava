from django.urls import path
from . import views
from .views import signup

from .views import TrackDetailView, AlbumListView

urlpatterns = [
    path('artists/', views.ArtistListView.as_view(), name='artist-list'),
    path('albums/', views.AlbumListView.as_view(), name='album-list'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('tracks/', views.TrackListView.as_view(), name='track-list'),
    path('tracks/<int:pk>/purchase/', views.TrackPurchaseView.as_view(), name='track-purchase'),
    path('signup/', signup, name='signup'),
    path('show_albums/', views.show_albums, name='show_albums'),
    path('latest_albums/', views.latest_albums_view, name='latest_albums_view'),
    path('most-viewed-albums/', views.most_viewed_albums_view, name='most_viewed_albums'),
    path('tracks/<int:pk>/', views.show_tracks, name='tracks'),
    path('latest-tracks/', views.latest_tracks_view, name='latest_tracks'),
    path('most-viewed-tracks/', views.most_viewed_tracks_view, name='most_viewed_tracks'),
    path('searchs/', views.search_view, name='searchs'),
    path('artist/<int:pk>/', views.artist_view, name='artist'),
    path('arts/', views.artists_list_view, name='arts'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
]
