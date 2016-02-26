from bnlipsum.lyrics.models import Track


def generate(words=50, paragraphs=1, ignore_chorus=False):
    paras = []
    q = {}

    if ignore_chorus:
        q['chorus'] = False

    while len(paras) < paragraphs:
        para = ''
        words_in_para = para.split(' ')
        while not words or len(words_in_para) < words:
            track = Track.objects.filter(**q).order_by('?')[0]
            left = paragraphs - len(paras)

            if left <= 0:
                left = 1

            para += ' '.join(
                track.stanzas.values_list('lyrics', flat=True)[:left]
            ).replace(
                '\n', ' '
            ).strip()

            words_in_para = para.split(' ')
            if not words:
                break

        paras.append(para.strip())

    return '\n\n'.join(paras)
