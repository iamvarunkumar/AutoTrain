from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html',)

def login(request):
    return render(request, 'signup.html')

def documentation(request):
    return render(request, 'documentation.html')

def dashboard(request):
    return render(request, 'dashboard.html')
