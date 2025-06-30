from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def compare(request):
    return render(request, 'compare.html')
