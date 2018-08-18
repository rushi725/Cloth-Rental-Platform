from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from .models import CartP, Address, Order
from datetime import datetime 

User = get_user_model()

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username','email','password']

class OrderForm(forms.ModelForm):
	date_placed = forms.DateTimeField(initial=datetime.now(), required=False)
	class Meta:
		model = Order
		fields = ['shipping_address']
		

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


	
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get('password')
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This User Does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("This User is no longer active")




class CartForm(forms.ModelForm):

    class Meta:
        model = CartP
        fields = ['product', 'size','delivery_date']

class AddressForm(forms.ModelForm):

	class Meta:
		model = Address
		fields = ['first_name','last_name','address_line','city','state','pincode','phone_number']