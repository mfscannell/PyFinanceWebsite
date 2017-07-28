from django.shortcuts import render

# Create your views here.
def index(request):
    indexDict = {'idex_text': 'Text from index dictionary'}
    return render(request, 'stockViewer/index.html', context = indexDict)
