from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            context={'error': 'Invalid username or password'}
            return render(request, 'accounts/login.html', context)
        login(request, user)
        return redirect('/')

    context={}
    
    return render(request, 'accounts/login.html', context)



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    context={}
    
    return render(request, 'accounts/logout.html', context=context)

def register_view(request):

    context={}
    
    return render(request, 'accounts/login.html', context=context)