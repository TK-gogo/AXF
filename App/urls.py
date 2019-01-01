from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^home/$', home, name='home'), #首页
    url(r'^market/(\d+)/(\d+)/(\d+)/$', market, name='market'), #闪购
    url(r'^cart/$', cart, name='cart'), #购物车
    url(r'^mine/$', mine, name='mine'), #我的
    url(r'^register/$', register, name='register'), #注册
    url(r'^register_handle/$', register_handle, name='register_handle'), #注册操作
    url(r'^check_username/$', check_username, name='check_username'),
    url(r'^login/$', login, name='login'),
    url(r'^login_handle/$', login_handle, name='login_handle'),
    url(r'^logout/$', logout, name='logout'), #注销
    url(r'^add_to_cart/$', add_to_cart, name='add_to_cart'), #添加到购物车
    url(r'^cart_num_add/$', cart_num_add, name='cart_num_add'), #购物车商品数量加1
    url(r'^cart_num_reduce/$', cart_num_reduce, name='cart_num_reduce'), #购物车商品数量减1
    url(r'^cart_del/$', cart_del, name='cart_del'), #购物车商品数量减1
    url(r'^cart_select/$', cart_select, name='cart_select'), #购物车商品选择不选
    url(r'^cart_select_all_or_none/$', cart_select_all_or_none, name='cart_select_all_or_none'), #购物车商品选择不选
]