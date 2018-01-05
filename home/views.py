from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse,redirect
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from home import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import json
import requests
from home import models
from django.db.models import Sum,Count



s = requests.Session()
# Create your views here.
'''
系统登入
'''
def userlogin(request):
    # name = request.COOKIES.get('name')
    # if name:
    #     return HttpResponseRedirect('/alluser')
    if request.method == 'POST':
        error = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            response = HttpResponseRedirect('/alluser')
            # response.set_cookie('name', username,max_age=100)
            return response
        else:
            error = '用户名或密码错误'
            return render(request, 'system/system_login.html', {'error':error})

    elif request.method == 'GET':
        return render(request, 'system/system_login.html')


'''
系统登出
'''
def userlogout(request):
    logout(request)
    return HttpResponse("成功退出该系统")

'''
用户登记
'''
def register(request):
    if request.method == 'GET':
        return render(request, 'system/register.html')
    elif request.method == 'POST':
        company = request.POST.get('company','')
        phone = request.POST.get('phone','')
        contact_name = request.POST.get('name','')
        contact_phone = request.POST.get('contact_phone','')
        pro = request.POST.get('province','')
        ci = request.POST.get('city','')
        town = request.POST.get('town','')
        city = {
            'pro':pro,
            'ci':ci,
            'town':town
        }
        address = request.POST.get('address','')
        email = request.POST.get('email','')
        we_chat = request.POST.get('weixin','')
        qq = request.POST.get('qq','')
        note = request.POST.get('note','')
        d_json = {
            'name':company,
            'phone':phone,
            'contact_name':contact_name,
            'contact_phone':contact_phone,
            'city':city,
            'address':address,
            'email':email,
            'we_chat':we_chat,
            'qq':qq,
            'note':note
        }
        c = models.Zhanhui.objects.create(**d_json)
        c.save()
        if c:
            url = 'http://59.110.6.179:9007/fcwz/create_partner'
            data = json.dumps(d_json)
            headers = {"Content-Type": "application/json"}
            r = requests.post(url,data=data,headers=headers)
            dict1 = json.loads(r.text)
            if 'error' in dict1['result'].keys():
                return render(request, 'port/../templates/reg_faild.html')
            else:
                username = dict1['result']['success']
                return render(request, 'system/reg_succed.html', {'username':username})
        else:
            return HttpResponse('注册信息失败')

'''
获取全部用户
'''
@login_required
def all_user(request):
    user= models.Zhanhui.objects.all()
    count = models.Zhanhui.objects.filter(status=1).count()
    return render(request, 'system/zhanhui.html', {'user':user, 'count':count})


'''
确认收款
'''
def Queren(request,id):
    succ = models.Zhanhui.objects.get(pk=id)
    succ.status =1
    succ.save()
    return HttpResponseRedirect('/alluser')

'''
打印合同
'''
def Hetong(request,id):
    succ = models.Zhanhui.objects.get(pk=id)
    return render(request,'dayin.html',{'succ':succ})

'''
单个用户详情
'''
def order(request,id):
    if request.method == 'GET':
        order_one = models.Zhanhui.objects.filter(pk=id).all()
        print(order_one)
        return render(request, 'system/boot.html', {'order':order_one})
    elif request.method == 'POST':
        pay_account = request.POST.get('pay_account','')
        pay_way = request.POST.get('pay_way','')
        if pay_way == "支付宝":
            zhifubao = request.POST.get('zhifubao','')
            data = {
                'pay_account': pay_account,
                'pay_way': pay_way,
                'zhifubao': zhifubao,
            }
            d = models.Zhanhui.objects.filter(pk=id).update(**data)
            print("更新的数据", d)
        elif pay_way == "银行转账" or pay_way == '刷卡':
            kahao = request.POST.get('kahao', '')
            bank = request.POST.get('bank1', '')
            data ={
                'pay_account': pay_account,
                'pay_way': pay_way,
                'kahao':kahao,
                'bank':bank
            }
            d = models.Zhanhui.objects.filter(pk=id).update(**data)
            print("更新的数据", d)
        elif pay_way == '微信':
            we_chat = request.POST.get('weixin','')
            print(we_chat)
            data = {
                'pay_account': pay_account,
                'pay_way': pay_way,
                'we_chat':we_chat
            }
            print('微信的数据',data)
            d = models.Zhanhui.objects.filter(pk=id).update(**data)
            print("更新的数据", d)



        return HttpResponseRedirect('/alluser')


'''
登录装饰器
'''
def auth(func):
    def inner(request,*args,**kwargs):
        v = request.COOKIES.get('cookie')
        print('打印出设置得cookie',v)
        if not v:
            r = request.path
            url = '/login/?next=' + r
            return redirect(url)
        return func(request,*args,**kwargs)
    return inner


'''
登录页面
'''
def log_in(request):
    global s
    if request.method == 'GET':
        form = forms.LoginForm()
        return render(request, 'port/login.html', {'form':form})
    elif request.method == 'POST':
        form  = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uname']
            password = form.cleaned_data['pwd']

            url = 'http://59.110.6.179:9007/fcwz/userlogin/login'
            data = {'login':username,'password':password}
            r = s.post(url,data=data)
            dict1 = json.loads(r.text)
            if 'error' in dict1.keys():
                return render(request, 'port/login.html', {'form':form, 'error':dict1['error']})
            else:
                r = request.POST.get('next', '')
                if r:
                    response = HttpResponseRedirect(r)
                else:
                    response = HttpResponseRedirect('/address')
                cookie = dict1['session_id']
                print('返回给我得' + cookie)
                response.set_cookie('cookie', cookie, max_age=100)
                response.set_cookie('user', username, max_age=100)
                return response
        else:
            return render(request, 'port/login.html', {'form':form})


'''
新增收货地址
'''
@auth
def address(request):
    if request.method == 'GET':
        v = request.COOKIES.get('user')
        return render(request, 'port/add_address.html', {'current_user':v})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        pro = request.POST.get('province', '')
        ci = request.POST.get('city', '')
        town = request.POST.get('town', '')
        city = {
            'pro': pro,
            'ci': ci,
            'town': town
        }
        address = request.POST.get('address', '')
        we_chat = request.POST.get('weixin','')
        qq = request.POST.get('qq', '')
        note = request.POST.get('note', '')
        d_json = {
            'name': name,
            'email': email,
            'phone': phone,
            'city': city,
            'address': address,
            'we_chat': we_chat,
            'qq': qq,
            'note': note
        }
    data = json.dumps(d_json)
    url = 'http://59.110.6.179:9007/fcwz/create_shop_address'
    # cookie = request.COOKIES.get('cookie', '')
    # print('这是获取得cookies' + cookie)
    headers = {"Content-Type": "application/json"}
    global s
    r = s.post(url, data=data, headers=headers)
    print(r.headers)
    dict1 = json.loads(r.text)
    print(dict1)
    if 'error' in dict1['result'].keys():
        return render(request, 'port/add_address.html', {'error':dict1['result']['error']})
    else:
        response = HttpResponse('创建收货地址成功')
        return response





# @auth
# def get_order(request):
#     if request.method == 'GET':
#         v = request.COOKIES.get('user')
#         return render(request,'per_center.html',{'current_user':v})
#     elif request.method == 'POST':
#         order_code = request.POST.get('order_code','')
#         page = request.POST.get('page','')
#         size = request.POST.get('size','')
#         print(order_code,page,size)
#         d_json = {
#             'order_code':order_code,
#             'page':page,
#             'size':size
#         }
#         data = json.dumps(d_json)
#         url='http://59.110.6.179:9007/fcwz/get_sale_order_line'
#         headers = {"Content-Type": "x-www-form-urlencoded"}
#         cookies = request.COOKIES.get('cookie', '')
#         print("打印出来的cookie",cookies)
#         global s
#         r = s.post(url, data=data, headers=headers)
#         print(r.text)
#         dict1 = json.loads(r.text)
#         print(dict1)
#         return render(request,'per_center.html',{'detail':dict1})


'''
请求充值记录
'''
@auth
def get_payment(request):
    global s
    v = request.COOKIES.get('user')
    order_code = request.GET.get('order_code', '')
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 10)
    print("获取的查询数据",order_code, page, size)
    d_json = {

        'page': page,
        'size': size,
        'order_code': order_code

    }
    print("这是data数据",d_json)
    url = 'http://59.110.6.179:9007/fcwz/get_sale_order'
    headers = {"Content-Type": "x-www-form-urlencoded"}
    r = s.post(url, data=d_json, headers=headers)
    print(r.text)
    dict1 = json.loads(r.text)
    r1 = s.get('http://59.110.6.179:9007/fcwz/get_customer_payment')
    pay_data = r1.json()
    r2 = s.get('http://59.110.6.179:9007/fcwz/get_customer_balance')
    balance = r2.json()
    return render(request, 'port/per_center.html', {'user':v, 'pay_data':pay_data, 'balance': balance, 'dict1': dict1})
