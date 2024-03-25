from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,DetailView,TemplateView
from CakeBox.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from CakeBox.models import CakeVariant,Cake

# Create your views here.

class HomeView(TemplateView):
    template_name="home.html"

#url:localhost:8000/register/
#method:get,post
#form_class:RegistrationForm

class SignUpView(View):
    
    def get(self,request,*args, **kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args, **kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"register.html",{"form":form})
    
#url:localhost:8000/
#method:get,post
#form_class:LoginForm

class SignInView(View):
    
    
    def get(self,request,*args, **kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
            
        messages.error(request,"Invalid Credentials")
        
        return render(request,"signin.html",{"form":form})
    
 
#url:localhost:8000/index/
#method:get
class IndexView(View):
    def get(self,request,*args, **kwargs):
        qs=Cake.objects.all()
        return render(request,"index.html",{"data":qs})


#url:localhost:8000/cake/{id}/
# class CakeDetailView(DetailView):
#     template_name="detail.html"
#     model=CakeVariant
#     context_object_name="data"
    
# class CakeDetailView(View):
#     def get(self,request,*args, **kwargs):
#         id=kwargs.get("pk")
#         qs=CakeVariant.objects.get(id=id)
#         return render(request,"detail.html",{"data":qs})

class CakeDetailView(View):
    def get(self, request, *args, **kwargs):
        cake_id = kwargs.get("pk")
        cake_object=Cake.objects.get(id=cake_id)
        qs=CakeVariant.objects.filter(cake_object=cake_id)
        print(qs)
        return render(request, "detail.html",{"data":qs,"cake":cake_object})

