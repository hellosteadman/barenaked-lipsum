from django.template.response import TemplateResponse
from bnlipsum.lyrics.lipsum import generate


def lipsum(request):
    q = {}
    if request.GET.get('p'):
        try:
            q['paragraphs'] = int(request.GET['p'])
        except:
            pass

    if request.GET.get('w'):
        try:
            q['words'] = int(request.GET['w'])
        except:
            pass

    if request.GET.get('nc') == '1':
        q['ignore_chorus'] = True

    return TemplateResponse(
        request,
        'lyrics/lipsum.html',
        {
            'text': generate(**q)
        }
    )
