from django.contrib import admin
from bnlipsum.lyrics.models import Album, Track, Stanza


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')


class StanzaInline(admin.StackedInline):
    model = Stanza


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'album')
    list_filter = ('album',)
    inlines = [StanzaInline]
