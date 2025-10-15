from django.shortcuts import render


def home(request):
    return render(request, 'construction/index.html')  # adjust path per app