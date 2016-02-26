from django.db import models
from django.utils.translation import ugettext_lazy as _


class Album(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    artwork = models.ImageField(upload_to='albums', max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('year', 'title')


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('number',)
        unique_together = ('number', 'album')


class Stanza(models.Model):
    track = models.ForeignKey(Track, related_name='stanzas')
    number = models.PositiveIntegerField()
    lyrics = models.TextField()
    chorus = models.BooleanField(default=False)

    def __unicode__(self):
        return self.chorus and _('Chorus') or (_('Verse %d') % self.number)

    class Meta:
        ordering = ('number', 'track')
