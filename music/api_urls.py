from django.urls import path
from . import views
from music import views
from .views import AlbumListView, TrackDetailView, SearchViewAPI,GetAlbumsByArtistViewAPI

urlpatterns = [
    path('signup/', views.signup, name='api_signup'),
    path('login/', views.login_view, name='api_login'),


    path('albums/<int:album_id>/tracks/', views.TrackListByIDView.as_view(), name='track-list-ID'),

    path('track/<int:pk>/', TrackDetailView.as_view(), name='track_detail'),
    path('tracks/', views.TrackListView.as_view(), name='track-list'),
    path('signup/', views.signup, name='api_signup'),
    path('login/', views.login_view, name='api_login'),

    path('albums/', AlbumListView.as_view(), name='album-list'),

    path('latest-albums-api/', views.latest_albums_api_view, name='latest_albums_api'),
    path('most-viewed-albums-api/', views.most_viewed_albums_api_view, name='most_viewed_albums_api'),
    path('search/', SearchViewAPI.as_view(), name='search'),
    path('artist-album/', GetAlbumsByArtistViewAPI.as_view(), name='artist_album'),
]

