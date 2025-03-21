from django.shortcuts import render, redirect
from .forms import SignUpFormView
from django.contrib.auth import login
# Create your views here.
def homepage(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpFormView(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')
    else:
        form = SignUpFormView()

    return render(request, 'core/signup.html', {'form': form})
    