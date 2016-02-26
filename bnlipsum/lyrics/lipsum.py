from bnlipsum.lyrics.models import Track
import string


def generate(words=50, paragraphs=10, ignore_chorus=False):
    paras = []
    q = {}

    if ignore_chorus:
        q['chorus'] = False

    stanzas = []
    while len(paras) < paragraphs:
        para = ''
        words_in_para = [w for w in para.split(' ') if w.strip()]

        while not words or len(words_in_para) < words:
            if not any(stanzas):
                track = Track.objects.order_by('?')[0]
                stanzas = list(
                    track.stanzas.filter(**q).values_list('lyrics', flat=True)
                )

            left = paragraphs - len(paras)
            if left <= 0:
                left = 1

            if para:
                para += ' '

            stanza = stanzas.pop(0)
            if '<' in stanza:
                continue

            para += stanza.replace('\n', ' ').strip()
            words_in_para = [w for w in para.split(' ') if w.strip()]

            if not words:
                break
            elif len(words_in_para) > words:
                words_in_para = words_in_para[:words]
                para = ' '.join(words_in_para)

        if not para[-1] in string.punctuation:
            para += '.'

        paras.append(para.strip())

    return '\n\n'.join(paras)
