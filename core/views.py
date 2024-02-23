# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy 
# from django.contrib.auth.views import LoginView
# from django.views.generic.edit import FormView
# from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

# github sso settings
from django.conf import settings
import requests
from django.contrib.auth.models import User

# google auth
from django.urls import reverse

from .models import Errand
from .forms import ErrandForm, LoginForm, RegisterForm


#-------------------------------------------- CLASS BASED VIEWS -----------------------------------------------------

# class ErrandList(ListView):
#     model = Errand
#     context_object_name = "errands"
 

# class ErrandDetail(DetailView):
#     model = Errand


# class ErrandCreate(CreateView):
#     model = Errand
#     fields =  ['title', 'completed']
#     success_url = reverse_lazy('errands')
#     template_name = 'core/errand_create.html'
     

# class ErrandUpdate(UpdateView):
#     model = Errand
#     fields = ['title', 'completed']
#     success_url = reverse_lazy('errands')
#     template_name = 'core/errand_create.html'
 
# class ErrandDelete(DeleteView):
#     model = Errand
#     success_url = reverse_lazy('errands')
#     template_name = 'core/errand_delete.html'


# class Login(LoginView):
#     template_name = 'core/login.html'
#     field = '__all__'
#     redirect_authenticated_user = True
#     def get_success_url(self):
#         return reverse_lazy('errands')
    

# class Register(FormView):
#     template_name = "core/register.html"
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('errands')
#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             login(self.request, user=user)
#         return super(Register, self).form_valid(form)



#-------------------------------------------- FUNCTION BASED VIEWS -----------------------------------------------------

def github_login(request):
    # redirect users to GitHub's authorization page
    github_oauth_url = f"{settings.GITHUB_OAUTH_URL}?client_id={settings.GITHUB_CLIENT_ID}&scope=read:user"
    return redirect(github_oauth_url)

def github_callback(request):
    # code sent by GitHub to be exchanged for an access token
    code = request.GET.get('code')
    
    # exchange the code for an access token
    token_response = requests.post(
        settings.GITHUB_TOKEN_URL,
        data={
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code
        },
        headers={'Accept': 'application/json'}
    )
    
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    
    # use the access token to fetch the user's profile data from GitHub
    user_response = requests.get(
        settings.GITHUB_API_URL,
        headers={'Authorization': f'token {access_token}'}
    )
    
    user_data = user_response.json()
    
    # extract the GitHub username from the profile data
    github_username = user_data.get('login')
    name = user_data.get('name')
    first_name = name.split(" ")[0]
    last_name = name.split(" ")[1]
    
    # get the user by his GitHub username
    user = User.objects.filter(username=github_username).first()
    
    if user:
        # user exists, you could update user details here
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    else:
        # Create a new user if one does not exist
        user = User.objects.create_user(
            username=github_username,
            first_name = first_name,
            last_name = last_name,
        )
    
    login(request, user)
    
    # redirect to the homepage or dashboard after login
    return redirect('/')


def google_login(request):
    scope = "email profile"
    redirect_uri = 'http://127.0.0.1:8000/accounts/google/login/callback/'   
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}&access_type=offline&prompt=consent"

    return redirect(auth_url)

def google_callback(request):
    code = request.GET.get('code')

    # exchange the code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://127.0.0.1:8000/accounts/google/login/callback/',
        'grant_type': 'authorization_code',
    }
    
    token_response = requests.post(token_url, data=token_data)
    
    # it will raise an HTTPError if the HTTP request returned an unsuccessful status code
    token_response.raise_for_status()  
    token = token_response.json().get('access_token')

    # use the access token to access the Google API
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_r = requests.get(user_info_url, headers={'Authorization': f'Bearer {token}'})
    user_info = user_info_r.json()
    
    first_name = user_info['given_name']
    last_name = user_info['family_name']
    full_name = first_name + last_name[:2]
    
    user = User.objects.filter(username=full_name).first()

    if user:
        # user exists, you could update user details here
        user.first_name = user_info['given_name']
        user.last_name = user_info['family_name']
        user.email = user_info['email']
        user.save()
    else:
        # Create a new user if one does not exist
        user = User.objects.create_user(
            username=full_name,
            first_name = user_info['family_name'],
            last_name = user_info['given_name'],
            email = user_info['email'],
        )
        
    login(request, user)

    # redirect to the homepage or dashboard after login
    return redirect('/')


@login_required   
def errand_list(request):
    if request.method == "GET":
        # filer by field inside database and get only tasks of authentificated person
        errands = Errand.objects.filter(created_by=request.user)
        # num of unfinished task written on errand_list.html 
        incompleted_tasks = len(errands.filter(completed=False)) 
        return render(request, 'core/errand_list.html', {
            'errands': errands,
            'incompleted_tasks': incompleted_tasks,
        })


@login_required
def errand_detail(request, pk):
    if request.method == "GET":
        errand = Errand.objects.get(pk=pk)
        return render(request, 'core/errand_detail.html', {
            'errand': errand
        })


@login_required 
def errand_create(request):
    if request.method == "POST":
        form = ErrandForm(request.POST)
        if form.is_valid():
            errand = form.save(commit=False)
            errand.created_by = request.user
            errand.save()
            return redirect('errands')
    else:
        form = ErrandForm()
    return render(request, 'core/errand_create.html', {
        'form': form
    })


@login_required
def errand_update(request, pk):
    errand = get_object_or_404(Errand, pk=pk)
    if request.method == "POST":
        form = ErrandForm(request.POST, instance=errand)
        if form.is_valid():
            errand = form.save(commit=False)
            errand.save()
            return redirect('errands') # return redirect('detail', pk=errand.pk)
    else:
        form = ErrandForm(instance=errand)
    return render(request, 'core/errand_create.html', {
        'form': form
    })


@login_required
def errand_delete(request, pk):
    errand = get_object_or_404(Errand, pk=pk)
    errand.delete()
    return redirect('errands')

# @login_required
# def errand_delete(request, pk):
#     errand = get_object_or_404(Errand, pk=pk)
#     if request.method == "POST":   
#         errand.delete()
#         return redirect('errands')
#     return render(request, 'core/errand_delete.html', {
#         'errand': errand
#     })


def errand_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user=user)
                return redirect('errands')
            else:
                messages.error(request, '* Invalid login name or password. Please try again.')
            
    return render(request, 'core/login.html', {
        'form': form,
    })
  
  
def errand_logout(request):
    logout(request)
    return redirect('errands')
    
    
def errand_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('errands')
    else:    
        form = RegisterForm()
        
    return render(request, template_name='core/register.html', context={
        'form': form
    })