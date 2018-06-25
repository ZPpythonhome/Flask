from django.conf.urls import url

from AXF import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<categoryid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_parmas, name='market_with_params'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^userregister/', views.user_register, name='user_register'),
    url(r'^userlogout/', views.user_logout, name='user_logout'),
    url(r'^checkuser/', views.check_user, name='check_user'),
    url(r'^checkemail/', views.check_email, name='check_email'),
    url(r'^userlogin/', views.user_login, name='user_login'),

    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^subtocart/', views.sub_to_cart, name='sub_to_cart'),
    url(r'^changecartstatus/', views.change_cart_status, name='change_cart_status'),
    url(r'^changecartsstatus/', views.change_carts_status, name='change_carts_status'),
    url(r'^makeorder/', views.make_order, name='make_order'),
    url(r'^orderdetail/', views.order_detail, name='order_detail'),
    url(r'^alipay/', views.alipay, name='alipay'),
    url(r'^orderlist/', views.order_list, name='order_list'),

    # 测试邮件
    url(r'^activeuser/', views.active_user),
]