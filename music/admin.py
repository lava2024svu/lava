from django.contrib import admin
from django.contrib.auth.models import User
from .models import Artist, Album, Track, Purchased

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio', 'image')  
    search_fields = ('name',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Distributors').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Distributors').exists()

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'cover_image' , 'category',)  
    list_filter = ('artist',)
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.created_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user) 

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.created_by == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.created_by == request.user
    
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'duration', 'audio_file',)  
    list_filter = ('album',)
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.created_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user) 

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.created_by == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.created_by == request.user

class PurchasedAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'purchase_date', 'end_date')
    list_filter = ('user',)
    search_fields = ('track__title',)

# تسجيل النماذج مع الإعدادات الخاصة بها
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Purchased, PurchasedAdmin)







# change name of titles and header in dashboard

from django.contrib import admin

admin.site.site_header = "Dashboard" 
admin.site.site_title = "Alhani - Dashboard"  
admin.site.index_title = "Welcome to Alhani - Dashboard" 
