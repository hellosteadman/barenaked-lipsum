from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from logging import getLogger
from bnlipsum.lyrics import helpers
from bnlipsum.lyrics.models import Album, Track, Stanza
import time


class Command(BaseCommand):
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('artist', nargs='+', type=str)

    def handle(self, *args, **options):
        logger = getLogger('bnlipsum.lyrics')
        for artist in options['artist']:
            with atomic():
                letter = artist[0]
                url = 'http://www.azlyrics.com/%s/%s.html' % (letter, artist)
                logger.info(u'Looking for albums by %s' % artist)

                for (album, year, tracks) in helpers.get_albums(url):
                    logger.info(
                        u'Found album ("%s") with %d track(s)' % (
                            album, len(tracks)
                        )
                    )

                    try:
                        album = Album.objects.get(
                            title__iexact=album,
                            year=year
                        )
                    except Album.DoesNotExist:
                        album = Album.objects.create(
                            title=album,
                            year=year
                        )

                        for i, (title, url) in enumerate(tracks):
                            logger.info(u'Parsing lyrics to "%s"' % title)
                            lyrics = helpers.get_lyrics(url)

                            if lyrics is None:
                                continue

                            try:
                                track = album.tracks.get(
                                    number=i + 1
                                )
                            except Track.DoesNotExist:
                                track = album.tracks.create(
                                    title=title,
                                    number=i + 1
                                )

                            for n, (text, chorus) in enumerate(lyrics):
                                try:
                                    stanza = track.stanzas.get(
                                        number=n + 1
                                    )
                                except Stanza.DoesNotExist:
                                    stanza = Stanza(
                                        track=track,
                                        number=n + 1
                                    )

                                stanza.chorus = chorus
                                stanza.lyrics = text
                                stanza.save()

                            time.sleep(1)
