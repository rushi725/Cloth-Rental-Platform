from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

# Create your models here.
class Address(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	address_line = models.CharField(max_length=500)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	pincode = models.IntegerField()
	phone_number = models.IntegerField()
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

class Product(models.Model):
	category = models.ForeignKey(
	    'Category',
	    on_delete=models.CASCADE,
	    null=True,
	    blank=True,
	    related_name='category')
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)

	XS, S, M, L, XL, XXL  = ('XS', 'S', 'M', 'L', 'XL', 'XXL')
	SIZE_CHOICES = (
	    (XS, _("XS")),
	    (S, _("S")),
	    (M, _("M")),
	    (L, _("L")),
	    (XL, _("XL")),
	    (XXL, _("XXL")),
	)
	pimage = models.FileField(null=True)


	price = models.IntegerField()
	def __str__(self):
		return self.title + '-'+ self.category.title

	def get_absolute_url(self):
		return reverse('welcome:detail',kwargs={'pk':self.pk})

class Image(models.Model):
	product = models.ForeignKey(
	    'Product',
	    on_delete=models.CASCADE,
	    related_name='images')
	original = models.FileField()
	caption = models.CharField(max_length=200, blank=True)

	#: Use display_order to determine which is the "primary" image
	display_order = models.PositiveIntegerField(default=0)
	def __str__(self):
		return self.product.title 



class CartP(models.Model):
	user = models.ForeignKey(
        User, related_name='cart', null=True, blank=True,
        on_delete=models.SET_NULL)

	product = models.ForeignKey(
	    'Product',
	    on_delete=models.CASCADE)
	size = models.CharField(max_length=10)
	delivery_date = models.DateField()

	def __str__(self):
		return self.user.username + '-' + self.product.title

class Order(models.Model):

    # Orders can be placed without the user authenticating so we don't always
    # have a customer ID.
	user = models.ForeignKey(
        User, related_name='orders', null=True, blank=True,
        on_delete=models.SET_NULL)

	shipping_address = models.ForeignKey(
        'Address', null=True, blank=True,
        on_delete=models.SET_NULL)


    # Index added to this field for reporting
	date_placed = models.DateTimeField(auto_now=True,blank=True)
	def __str__(self):
		return self.user.username

class Category(models.Model):
	title = models.CharField(max_length=255)
	image = models.FileField()
	MEN, WOMEN, KIDS = ('Men', 'Women', 'Kids')
	GENDER_CHOICES = (
        (MEN, _("Men")),
        (WOMEN, _("Women")),
        (KIDS, _("Kids")),
    )

	gender = models.CharField(
    	pgettext_lazy(u"Product is available for", u"Available_for"),
	    max_length=64, choices=GENDER_CHOICES)

	"""def get_absolute_url(self):
		return reverse('welcome:products',kwargs={'pk':self.pk})"""

	def __str__(self):
		return self.title + '-'+ self.gender

		

		





		
		
