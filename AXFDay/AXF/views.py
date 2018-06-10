import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from AXF import order_status
from AXF.models import HomeWheel, HomeNav, HomeMustBuy, HomeShop, HomeMainShow, Foodtype, Goods, UserModel, CartModel, \
    OrderModel, OrderGoods

ALL_TYPE = '0'
ORDER_TOTAL = '0'
PRICE_ASC = '1'
PRICE_DESC = '2'


def home(request):
    wheels = HomeWheel.objects.all()

    navs = HomeNav.objects.all()

    mustbuys = HomeMustBuy.objects.all()

    shops = HomeShop.objects.all()

    shops0_1 = shops[0:1]

    shops1_3 = shops[1:3]

    shops3_7 = shops[3:7]

    shops7_11 = shops[7:11]

    mainshows = HomeMainShow.objects.all()

    data = {
        'title': '首页',
        "wheels": wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shops0_1': shops0_1,
        'shops1_3': shops1_3,
        'shops3_7': shops3_7,
        'shops7_11': shops7_11,
        'mainshows': mainshows,
    }

    return render(request, 'home/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={"categoryid": 104749, 'childcid': 0, 'order_rule': 0}))


def market_with_parmas(request, categoryid, childcid, order_rule):
    foodtyps = Foodtype.objects.all()

    if childcid == ALL_TYPE:
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childcid)

    foodtype = Foodtype.objects.get(typeid=categoryid)
    """
        order_rule
            0   代表综合排序
            1   代表价格升序
            2   代表价格降序
            3   竞价排名
    """
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == PRICE_ASC:
        goods_list = goods_list.order_by("price")
    elif order_rule == PRICE_DESC:
        goods_list = goods_list.order_by("-price")

    """
        全部类型:0#进口水果:110#国产水果:120
    """
    childtypenames = foodtype.childtypenames
    """
        [全部类型:0, 进口水果:110, 国产水果:120]
    """
    childtypename_list = childtypenames.split("#")

    child_type_list = []
    """
        [[全部类型, 0], [进口水果, 110], [国产水果, 120]]
    """
    for childtypename in childtypename_list:
        child_type_list.append(childtypename.split(":"))

    data = {
        'title': '闪购',
        'foodtypes': foodtyps,
        'goods_list': goods_list,
        'categoryid': int(categoryid),
        'child_type_list': child_type_list,
        'childcid': childcid,
        'order_rule': order_rule,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    userid = request.session.get('user_id')

    if not userid:
        return redirect(reverse('axf:user_login'))

    user = UserModel.objects.get(pk=userid)

    cartmodels = user.cartmodel_set.all()

    is_all_select = True

    total_price = 0

    for cartmodel in cartmodels:
        if not cartmodel.c_goods_select:
            is_all_select = False
        else:
            total_price += cartmodel.c_goods_num * cartmodel.c_goods.price

    data = {
        'title': '购物车',
        'cartmodels': cartmodels,
        'is_all_select': is_all_select,
        'total_price': '{:.2f}'.format(total_price)
    }

    return render(request, 'cart/cart.html', context=data)


def mine(request):
    is_login = False

    user_id = request.session.get('user_id')

    data = {
        'title': '我的',
        'is_login': is_login,
    }

    if user_id:
        is_login = True
        user = UserModel.objects.get(pk=user_id)
        data['is_login'] = is_login
        data['user_icon'] = '/static/upload/' + user.u_icon.url
        data['username'] = user.u_name
        ordered_count = OrderModel.objects.filter(o_user=user).filter(o_status=order_status.ORDERED).count()
        if ordered_count > 0:
            data['ordered_count'] = ordered_count
        wait_receive_count = OrderModel.objects.filter(o_user=user).filter(o_status=order_status.PAYED).count()
        if wait_receive_count > 0:
            data['wait_receive_count'] = wait_receive_count

    return render(request, 'mine/mine.html', context=data)


def user_register(request):
    if request.method == "GET":

        data = {
            "title": '用户注册'
        }
        return render(request, 'user/user_register.html', context=data)
    elif request.method == "POST":

        username = request.POST.get('u_name')
        password = request.POST.get('u_password')
        email = request.POST.get('u_email')
        icon = request.FILES.get('u_icon')

        print(password)

        user = UserModel()

        user.u_name = username
        user.u_email = email
        user.u_icon = icon

        user.set_password(password)

        user.save()

        request.session['user_id'] = user.id

        send_mail_learn(username, email, user.id)

        return redirect(reverse('axf:mine'))


def user_logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def check_user(request):
    username = request.GET.get("u_name")
    # 0 或 1
    users = UserModel.objects.filter(u_name=username)

    data = {
        'status': '200',
        'msg': 'ok'
    }

    if users.exists():
        # 801 代表用户已存在
        data['status'] = '801'
        data['msg'] = 'already exists'
    else:
        data['msg'] = 'can use'

    return JsonResponse(data)


def check_email(request):
    email = request.GET.get('u_email')

    users = UserModel.objects.filter(u_email=email)

    data = {
        'status': '200',
        'msg': 'ok'
    }

    if users.exists():
        data['status'] = '802'
        data['msg'] = 'email already exists'
    else:
        data['msg'] = 'can use'

    return JsonResponse(data)


def user_login(request):
    if request.method == "GET":

        msg = request.session.get('msg')

        data = {
            'title': '用户登录',
            'msg': msg
        }

        return render(request, 'user/user_login.html', context=data)
    elif request.method == "POST":

        username = request.POST.get('u_name')
        password = request.POST.get('u_password')

        users = UserModel.objects.filter(u_name=username)

        if users.exists():
            user = users.first()

            if user.check_password(password):
                if not user.is_active:
                    request.session['msg'] = '用户未激活'
                    return redirect(reverse('axf:user_login'))

                request.session['user_id'] = user.id
                return redirect(reverse('axf:mine'))
            else:
                request.session['msg'] = '密码错误'
                # 密码错误
                return redirect(reverse('axf:user_login'))
        else:
            request.session['msg'] = '用户不存在'
            # 用户不存在
            return redirect(reverse('axf:user_login'))


"""
激活
    能找到用户的方式
        - 根据用户唯一标识
    修改用户状态
"""


def send_mail_learn(username, email, userid):
    subject = '爱鲜蜂VIP激活邮件'

    message = ""

    recipient_list = [email, ]

    temp = loader.get_template('user/user_active.html')

    token = str(uuid.uuid4())

    cache.set(token, userid, timeout=60 * 60)

    data = {
        'username': username,
        'active_url': 'http://127.0.0.1:8001/axf/activeuser/?utoken=%s' % token,
    }

    html = temp.render(data)

    send_mail(subject, message, 'rongjiawei1204@163.com', recipient_list, html_message=html)


def active_user(request):
    user_token = request.GET.get('utoken')

    user_id = cache.get(user_token)

    cache.delete(user_token)

    if not user_id:
        return HttpResponse("激活已过期，请重新申请激活邮件")
    user = UserModel.objects.get(pk=user_id)

    user.is_active = True

    user.save()

    return HttpResponse('用户激活成功')


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')

    userid = request.session.get('user_id')

    print(goodsid)

    data = {
        'status': '200',
        'msg': 'ok'
    }

    if not userid:
        data['status'] = '302'
        data['msg'] = 'not login'
    else:
        # 数据添加
        goods = Goods.objects.get(pk=goodsid)
        user = UserModel.objects.get(pk=userid)

        cartmodels = CartModel.objects.filter(c_goods=goods).filter(c_user=user)

        # cartmodels = CartModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        # 至多也就一个
        if cartmodels.exists():
            cartmodel = cartmodels.first()
            cartmodel.c_goods_num = cartmodel.c_goods_num + 1
            cartmodel.save()
        else:
            cartmodel = CartModel()
            cartmodel.c_goods = goods
            cartmodel.c_user = user
            cartmodel.save()

        data['goods_num'] = cartmodel.c_goods_num

    return JsonResponse(data)


def sub_to_cart(request):
    cartid = request.GET.get('cartid')

    cart_model = CartModel.objects.get(pk=cartid)

    data = {
        'status': '200',
        'msg': 'ok'
    }

    if cart_model.c_goods_num == 1:
        cart_model.delete()
        data['goods_num'] = 0
    else:
        cart_model.c_goods_num = cart_model.c_goods_num - 1
        cart_model.save()
        data['goods_num'] = cart_model.c_goods_num

    data['total_price'] = '{:.2f}'.format(calc_total(request.session.get('user_id')))

    return JsonResponse(data)


def change_cart_status(request):
    carid = request.GET.get('cartid')

    cartmodel = CartModel.objects.get(pk=carid)

    cartmodel.c_goods_select = not cartmodel.c_goods_select

    cartmodel.save()

    is_all_select = True

    userid = request.session.get('user_id')

    cartmodels = CartModel.objects.filter(c_user_id=userid).filter(c_goods_select=False)

    if cartmodels.exists():
        is_all_select = False

    data = {
        'status': '200',
        'msg': 'ok',
        'is_select': cartmodel.c_goods_select,
        'is_all_select': is_all_select,
        'total_price': '{:.2f}'.format(calc_total(userid))
    }

    return JsonResponse(data)


def change_carts_status(request):
    carts = request.GET.get('carts')

    print(carts)

    cart_list = carts.split("#")

    print(cart_list)

    select = request.GET.get('select')

    print(select)

    print(type(select))

    if select == 'true':
        print('选中')
        is_select = True
    else:
        print('未选中')
        is_select = False

    for cartid in cart_list:
        cartmodel = CartModel.objects.get(pk=cartid)
        cartmodel.c_goods_select = is_select
        cartmodel.save()

    data = {
        'msg': 'ok',
        'status': '200',
        'total_price': '{:.2f}'.format(calc_total(request.session.get('user_id')))
    }

    return JsonResponse(data)


def calc_total(user_id):
    cartmodels = CartModel.objects.filter(c_user_id=user_id).filter(c_goods_select=True)

    total_price = 0

    for cartmodel in cartmodels:
        total_price += cartmodel.c_goods_num * cartmodel.c_goods.price

    return total_price


def make_order(request):

    carts = request.GET.get('carts')

    cart_list = carts.split('#')

    print(cart_list)

    """
        从购物车到订单
            - 从购物车中查出需要下单的数据
            - 生成一个订单
            - 生成订单商品信息（购物车表中导出）
            - 删除购物车数据
    """

    userid = request.session.get('user_id')
    # 生成订单
    order = OrderModel()
    # 订单绑定用户
    order.o_user_id = userid

    order.save()
    # 导数据
    for cartid in cart_list:
        # 查出购物车中欲购买数据
        cartmodel = CartModel.objects.get(pk=cartid)
        # 生成要买的订单数据
        ordergoods = OrderGoods()
        # 指定订单
        ordergoods.o_order = order
        # 设置相关信息
        ordergoods.o_goods = cartmodel.c_goods

        ordergoods.o_goods_num = cartmodel.c_goods_num
        # 存入数据库
        ordergoods.save()
        # 删除购物车中的信息
        cartmodel.delete()

    data = {
        'msg': 'ok',
        'status': '200',
        'orderid': order.id
    }

    return JsonResponse(data)


def order_detail(request):

    order_id = request.GET.get('order_id')

    order = OrderModel.objects.get(pk=order_id)
    #  隐形属性  主获取从的隐性属性， manager对象
    # order.ordergoods_set

    data = {
        'order': order
    }

    return render(request, 'order/order_detail.html', context=data)


def alipay(request):

    orderid = request.GET.get('orderid')

    order = OrderModel.objects.get(pk=orderid)

    order.o_status = order_status.PAYED

    order.save()

    data = {
        'status': '200',
        'msg': 'ok'
    }

    return JsonResponse(data)


def order_list(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect(reverse('axf:user_login'))

    o_status = request.GET.get('status')

    if o_status:
        orders = OrderModel.objects.filter(o_user_id=user_id).filter(o_status=o_status)
    else:
        orders = OrderModel.objects.filter(o_user_id=user_id)

    data = {
        'orders': orders
    }

    return render(request, 'order/order_list.html', context=data)