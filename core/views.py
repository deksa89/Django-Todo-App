from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

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
#     template_name = 'core/errand_create.html' # obavezno unesi cijeli path, tako da ukljucuje i glavni folder u ovom slucaju je to 'core'
     

# class ErrandUpdate(UpdateView):
#     model = Errand
#     fields = ['title', 'completed']
#     success_url = reverse_lazy('errands')
#     template_name = 'core/errand_create.html'  # ako je u CreateView-u template name izmjenjeno to znaci da ga trebamo i u UpdateView-u izmjeniti

 
# class ErrandDelete(DeleteView):
#     model = Errand
#     success_url = reverse_lazy('errands')
#     template_name = 'core/errand_delete.html'


# class Login(LoginView):
#     template_name = 'core/login.html'
#     field = '__all__'
#     redirect_authenticated_user = True  # kada smo logirani vraca nas na pocetnu stranicu    
#     def get_success_url(self):
#         return reverse_lazy('errands')
    

# class Register(FormView):
#     template_name = "core/register.html"
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('errands')
#     def form_valid(self, form): # BEZ NJE SE NEMOZEMO REGISTRIRATI 
#         user = form.save()
#         if user is not None:
#             login(self.request, user=user)
#         return super(Register, self).form_valid(form)



#-------------------------------------------- FUNCTION BASED VIEWS -----------------------------------------------------

@login_required   
def errand_list(request):
    if request.method == "GET":
        errands = Errand.objects.filter(created_by=request.user)  # filtriramo po polju unutar baze podataka i ispisujemo samo taskove koje je autentificirana osoba kreirala

        return render(request, 'core/errand_list.html', {
            'errands': errands
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
            return redirect('errands') # ako zelis vidjeti kreirani task: return redirect('detail', pk=errand.pk), to ce nas preusmjeriti na detail url
        
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


# @login_required
# def errand_delete(request, pk):  # OVA FUNKCIJA NAS NE VODI DO HTML STRANICE NA KOJOJ POTVRDUJEMO DA ZELIMO OBRISATI NEKI TASK VEC IH ODMAH BRISE
#     errand = get_object_or_404(Errand, pk=pk)
#     errand.delete()
#     return redirect('errands')

@login_required
def errand_delete(request, pk):
    errand = get_object_or_404(Errand, pk=pk)
    if request.method == "POST":   
        errand.delete()
        return redirect('errands')
    return render(request, 'core/errand_delete.html', {
        'errand': errand
    })


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
                            
    return render(request, 'core/login.html', {
        'form': form,
    })
  
  
#DODANO KAO FUNCTION-BASED VIEWS, U KLASNIMA JE LOGOUT U VIEWS.PY
def errand_logout(request):
    logout(request)
    return redirect('errands')
    
    
def errand_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('errands')
    form = RegisterForm
    return render(request, template_name='core/register.html', context={
        'form': form
    })