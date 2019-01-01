import hashlib
import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from AXF.settings import MEDIA_ROOT
import uuid

#家
def home(request):

    #轮播图
    wheels = MainWheel.objects.all()

    #导航
    navs = MainNav.objects.all()

    # 必买
    mustbuys = MainMustbuy.objects.all()

    #shop
    shops = MainShop.objects.all()

    shop0 = shops[0]
    shop1_2 = shops[1:3]
    shop3_6 =shops[3:7]
    shop7_10 = shops[7:11]

    #主要商品
    shows = MainShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0':shop0,
        'shop1_2':shop1_2,
        'shop3_6':shop3_6,
        'shop7_10':shop7_10,
        'shows': shows
    }
    return render(request, 'home/home.html', data)


#闪购
def market(request,typeid,child_type_id,sortid):

    #取到所有分类数据
    food_types = FoodTypes.objects.all()

    #根据主分类id来筛选商品
    goods = Goods.objects.filter(categoryid=typeid)

    #当点击子分类时再筛选
    if child_type_id != '0':
        goods = goods.filter(childcid=child_type_id)

    #综合排序
    if sortid == '0':
        pass
    #销量排序
    elif sortid == '1':
        goods = goods.order_by('productnum')
    #价格降序
    elif sortid == '2':
        goods = goods.order_by('-price')
    #价格升序
    elif sortid == '3':
        goods = goods.order_by('price')

    #取到一条分类数据
    current_type = FoodTypes.objects.get(typeid=typeid)

    #子分类
    child_type_names = current_type.childtypenames

    child_type_list = child_type_names.split('#')

    print(child_type_list)
    #['全部分类:0', '酸奶乳酸菌:103537', '牛奶豆浆:103538', '面包蛋糕:103540']

    child_type_list = [child_type.split(':') for child_type in child_type_list]

    print(child_type_list)
    #[['全部分类', '0'], ['酸奶乳酸菌', '103537'], ['牛奶豆浆', '103538'], ['面包蛋糕', '103540']]

    data = {
        'food_types': food_types,
        'goods': goods,
        'typeid': typeid,
        'child_type_list': child_type_list,
        'child_type_id': child_type_id,
    }
    return render(request, 'market/market.html', data)

#购物车
def cart(request):

    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('axf:login'))

    carts = Cart.objects.filter(user_id=userid)


    return render(request, 'cart/cart.html', {'carts':carts})

#我的
def mine(request):
    data = {
        'username':'',
        'icon':'',
    }

    usreid = request.session.get('userid')

    users = User.objects.filter(id=usreid)

    if users:
        data['username'] = users.first().username
        data['icon'] = users.first().icon


    return render(request, 'mine/mine.html', data)


def my_md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()


#注册
def register(request):
    return render(request, 'user/register.html')

#注册操作
def register_handle(request):


    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon_file')


        if not username or not password or not re_password or not email:
            return HttpResponse('提交的内容有一项是空')

        if password != re_password:
            return HttpResponse('输入密码不一致')

        if User.objects.filter(username=username):
            return HttpResponse('该用户已经注册')

        user = User()
        user.username = username
        user.password = my_md5(password)
        user.email = email

        user.save()

        if icon:
            # 头像文件名 uuid + 上传文件的后缀
            icon_file_name = str(uuid.uuid4()) + os.path.splitext(icon.name)[1]

            #头像保存的硬盘路径
            file_save_path = MEDIA_ROOT + icon_file_name

            with open(file_save_path, 'ab') as f:
                for part in icon.chunks():
                    f.write(part)

            #数据库中保存的文件名
            db_save_path = '/uploads/' + icon_file_name

            user.icon = db_save_path

            user.save()



        return HttpResponse('注册成功')

    return HttpResponse('请求方法有误')


def check_username(request):

    if request.method == 'GET':
        username = request.GET.get('username')
        if username:
            if User.objects.filter(username=username):
                return JsonResponse({'status':0,'msg':'用户名已存在'})

            return JsonResponse({'status':1,'msg':'用户名可用'})

        return JsonResponse({'status':-1,'msg':'提交用户名是空'})

    return JsonResponse({'status':-2,'msg':'请求方式不对'})


def login(request):

    return render(request, 'user/login.html')


def login_handle(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        users = User.objects.filter(username=username, password=password)
        if users:

            #在session中保存用户id
            request.session['userid'] = users.first().id
            return redirect(reverse('axf:mine'))

        return HttpResponse('用户名或密码错误')

    return HttpResponse('请求方式不对')


def logout(request):

    del request.session['userid']

    return redirect(reverse('axf:mine'))

#添加到购物车
def add_to_cart(request):

    data = {
        'status':1,
        'msg':'成功',
    }

    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = '没有登录'
    else:
        if request.method == 'GET':

            goodsid = request.GET.get('goodsid')
            num = request.GET.get('num')

            # 查看当前用户购物中是否有商品
            carts = Cart.objects.filter(user_id=userid,goods_id=goodsid)

            #如果购物车存在
            if carts.exists():

                cart = carts.first()
                cart.num += int(num)
                cart.save()
            #如果不存在
            else:
                cart = Cart()
                cart.user_id = userid
                cart.goods_id = goodsid
                cart.num = int(num)
                # cart.is_select = True

                cart.save()

        else:
            data['status'] = -1
            data['msg'] = '请求方式不对'


    return JsonResponse(data)


def cart_num_add(request):

    data = {
        'status':1,
        'msg':'成功',
    }

    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = '没有登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')

            carts = Cart.objects.filter(id=cartid)

            if not carts:
                data['status'] = -1
                data['msg'] = 'no cart with this user'
            else:
                cart = carts.first()
                cart.num += 1

                cart.save()

                #把商品数量返回到前台
                data['num'] = cart.num

        else:
            data['status'] = -2
            data['msg'] = 'request error'


    return JsonResponse(data)


def cart_num_reduce(request):

    data = {
        'status':1,
        'msg':'成功',
    }

    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = '没有登录'
    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')

            carts = Cart.objects.filter(id=cartid)

            if not carts:
                data['status'] = -1
                data['msg'] = 'no cart with this user'
            else:
                cart = carts.first()

                #数量是否大于一
                if cart.num > 1:
                    cart.num -= 1

                cart.save()

                #把商品数量返回到前台
                data['num'] = cart.num

        else:
            data['status'] = -2
            data['msg'] = 'request error'


    return JsonResponse(data)


def cart_del(request):

    data = {
        'status':1,
        'msg':'成功',
    }

    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = '没有登录'
    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')


            #删除购车信息
            Cart.objects.filter(id=cartid,user_id=userid).delete()



        else:
            data['status'] = -2
            data['msg'] = 'request error'


    return JsonResponse(data)


def cart_select(request):

    data = {
        'status':1,
        'msg':'成功',
    }

    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = '没有登录'
    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')

            carts = Cart.objects.filter(id=cartid)
            if not carts:
                data['status'] = -1
                data['msg'] = '购物车中没有此商品'

            else:
                cart = carts.first()
                cart.is_select = not cart.is_select
                cart.save()

                #选择状态返回
                data['select'] = cart.is_select

        else:
            data['status'] = -2
            data['msg'] = 'request error'


    return JsonResponse(data)

def cart_select_all_or_none(request):

    data = {
        'status':1,
        'msg':'成功',
    }

    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = '没有登录'
    else:
        if request.method == 'POST':

            select = request.POST.get('select')

            if int(select):
                Cart.objects.filter(user_id=userid,is_select=False).update(is_select=True)

            else:

                Cart.objects.filter(user_id=userid, is_select=True).update(is_select=False)



        else:
            data['status'] = -2
            data['msg'] = 'request error'


    return JsonResponse(data)