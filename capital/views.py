from django.shortcuts import render


def home(request):
    return render(request, 'capital/index.html')  # adjust path per app