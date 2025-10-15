from django.shortcuts import render


def home(request):
    return render(request, 'resort/index.html')  # adjust path per app