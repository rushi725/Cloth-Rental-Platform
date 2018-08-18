from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.views import generic
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserLoginForm, CartForm, AddressForm, OrderForm
from django.views.generic import View
from .models import Category, Product, Image, CartP, Address
from django.db.models import Sum
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from datetime import datetime

# Create your views here.
form = CartForm()
form2 = AddressForm()
form3 = OrderForm()
form4 = UserForm()
def index(request):
	template = loader.get_template('welcome/index.html')
	product = Product.objects.all()[0:5]
	return render(request,'welcome/index.html',{'product' : product})

def shop_man(request):
	template = loader.get_template('welcome/shop.html')
	category = Category.objects.filter(gender='Men')
	return render(request,'welcome/shop.html',{'category' : category})

def shop_women(request):
	template = loader.get_template('welcome/shop.html')
	category = Category.objects.filter(gender='Women')
	return render(request,'welcome/shop.html',{'category' : category})

def shop_kids(request):
	template = loader.get_template('welcome/shop.html')
	category = Category.objects.filter(gender='Kids')
	return render(request,'welcome/shop.html',{'category' : category})

def products(request, gender, id):
	template = loader.get_template('welcome/shop.html')
	product = Product.objects.filter(category=id)
	return render(request,'welcome/products.html',{'products' : product})


class DetailView(DetailView):
	model = Product
	template_name = 'welcome/detail.html'



def cart(request):
	if request.method == "POST":
		forma = CartForm(request.POST)
		if forma.is_valid():
			post = forma.save(commit=False)
			post.user = request.user
			post.save()
			print("hello")
		else:
			print("not valid")		
	else:
		print("Hi")
	products = CartP.objects.filter(user__username=request.user)
	sumi = CartP.objects.filter(user__username=request.user).aggregate(Sum('product__price'))
	return render(request,'welcome/cart.html',{'sumi':sumi,'products':products,'form':form3})

class ProductDelete(DeleteView):
	model = CartP
	success_url = reverse_lazy('welcome:cart')

"""def checkoutStep1(request):
	template = loader.get_template('welcome/step1.html')
	addre = Address.objects.filter(user__username=request.user)
	return render(request,'welcome/step1.html',{'addre':addre,'form' : form2})"""

class AddressFormView(View):
	form_class = AddressForm
	template_name = 'welcome/step1.html'	

	def get(self,request):
		form = self.form_class(None)
		addre = Address.objects.filter(user__username=request.user)
		return render(request,self.template_name,{'form':form,'addre':addre})

	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()

		return redirect('/checkout/step2/%s/' % post.pk)

def checkoutStep2(request):
	template = loader.get_template('welcome/step2.html')
	return render(request,'welcome/step2.html')


def checkoutStep3(request,id):
	addr = Address.objects.get(pk=id)
	products = CartP.objects.filter(user__username=request.user)
	sumi = CartP.objects.filter(user__username=request.user).aggregate(Sum('product__price'))
	return render(request,'welcome/step3.html',{'products' : products,'a':addr,'sumi':sumi})

def checkoutStep4(request):
	if request.method == "POST":
		forma = OrderForm(request.POST)
		if forma.is_valid():
			post = forma.save(commit=False)
			post.user = request.user
			post.date_placed = datetime.now
			post.save()
			CartP.objects.filter(user__username=request.user).delete()
			print("hello")
			return render(request,'welcome/step4.html',{'number':post})
		else:
			print("not valid")		
	else:
		print("Hi")
	template = loader.get_template('welcome/step4.html')
	return render(request,'welcome/step4.html')


class UserFormView(View):
	form_class = UserForm
	template_name = 'welcome/login.html'	

	def get(self,request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form,'form2':form4})

	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			#cleaned (normalized) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#returns user objects if credential are correct
			user = authenticate(username=username,password=password)

			if user is not None:

				if user .is_active:
					login(request, user)
					return redirect('welcome:index')

		return render(request,self.template_name,{'form':form})


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'welcome/login.html'	

	def get(self,request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():
			
			#cleaned (normalized) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			#returns user objects if credential are correct
			user = authenticate(username=username,password=password)

			if user is not None:

				if user .is_active:
					login(request, user)
					print(request.user.is_authenticated())
					return redirect('welcome:index')


		return render(request,self.template_name,{'form':form})


def logout_view(request):
    logout(request)
    return redirect('welcome:index')