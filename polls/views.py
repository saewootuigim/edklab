from django.http import HttpResponse


def index(request):
    return HttpResponse("Eun Deok Kim's homepage")
