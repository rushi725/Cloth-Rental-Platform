

from django.conf.urls import include, url
from . import views

app_name = 'welcome'

urlpatterns = [
    #/game
    url(r'^$',views.index, name='index'),
    url(r'^cart/$',views.cart, name='cart'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$',views.logout_view, name="logout"),
    url(r'^register/$',views.UserFormView.as_view(), name='register'),

    url(r'^shop_man/$',views.shop_man, name='shop_man'),
    url(r'^shop_women/$',views.shop_women, name='shop_women'),
    url(r'^shop_kids/$',views.shop_kids, name='shop_kids'),

    url(r'^(?P<gender>\w+)/(?P<id>[0-9]+)/$',views.products,name='products'),

    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),

    url(r'(?P<pk>[0-9]+)/delete/$',views.ProductDelete.as_view(),name='product-delete'),


    url(r'^checkout/step1/$',views.AddressFormView.as_view(), name='step1'),
    url(r'^checkout/step2/$',views.checkoutStep2, name='step2'),
    url(r'^checkout/step2/(?P<id>[0-9]+)/$',views.checkoutStep3, name='step3'),
    url(r'^checkout/step3/$',views.checkoutStep4, name='step4'),

    ]