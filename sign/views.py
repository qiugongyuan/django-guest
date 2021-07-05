# from django.shortcuts import render
# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello Django!")
#
# # Create your views here.
import phone as phone
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
from sign.models import Guest
from django.shortcuts import get_object_or_404
def index(request):
    return render(request,"index.html")
def login_action(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)#登录
            request.session['user'] = username  # 将session信息记录到浏览器
            response= HttpResponseRedirect('/event_manage/')

            # if username=='admin' and password=='admin123':
        #     response= HttpResponseRedirect('/event_manage/')
        #    # response.set_cookie('user',username,3600)#添加浏览器cookie
        #     request.session['user']=username#将session信息记录到浏览器

            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
@login_required()
def event_manage(request):
    # username=request.COOKIES.get('user','')#读取浏览器cookie
    event_list=Event.objects.all()
    username=request.session.get('user','')#读取浏览器session
    return render(request,'event_manage.html',{"user":username,"events":event_list})
#发布会名称搜索
@login_required()
def search_name(request):
    username=request.session.get('user','')
    search_name=request.GET.get("name",'')
    event_list=Event.objects.filter(name__contains =search_name)
    return render(request,'event_manage.html',{"user":username,"events":event_list})

#嘉宾管理
@login_required()
def guest_manage(request):
    guest_list=Guest.objects.all()
    username=request.session.get('user','')#读取浏览器session
    return render(request,'guest_manage.html',{"user":username,"guests":guest_list})
#嘉宾手机搜索
@login_required()
def search_phone(request):
    username=request.session.get('user','')
    search_phone=request.GET.get("phone",'')
    guest_list=Guest.objects.filter(phone__contains =search_phone)
    return render(request,'guest_manage.html',{"user":username,"guests":guest_list})

#退出登录
@login_required()
def logout(request):
    auth.logout(request)#退出登录
    response=HttpResponseRedirect('/index/')
    return response
#签到页面
@login_required()
def sign_index(request,event_id):
    event_name=get_object_or_404(Event,id=event_id)
    # print("event_name:%s" % (dir(event_name)))
    # print("event_name:%s" % (event_name.name))
    return render(request,'sign_index.html',{'eventID':event_id,'eventName':event_name.name})
#签到动作
@login_required()
def sign_index_action(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)

    phone=request.POST.get('phone','')
    print(phone)

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'eventID': event_id, 'hint': 'phone error'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'eventID': event_id, 'hint': 'phone or event id error'})


    result = Guest.objects.filter(phone=phone, event_id=event_id)
    print(result.values())
    print(list(result.values()))
    print(list(result.values())[0]['sign'])
    result = list(result.values())[0]
    if result['sign']:
         return render(request, 'sign_index.html', {'eventID': event_id, 'hint': 'user has sign in'})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
    return render(request, 'sign_index.html', {'eventID': event_id, 'hint': 'sign in success', 'guest': result})





# 签到动作
# @login_required
# def sign_index_action(request,event_id):
#
#     event = get_object_or_404(Event, id=event_id)
#     guest_list = Guest.objects.filter(event_id=event_id)
#     guest_data = str(len(guest_list))
#     sign_data = 0   #计算发布会“已签到”的数量
#     for guest in guest_list:
#         if guest.sign == True:
#             sign_data += 1
#
#     phone =  request.POST.get('phone','')
#
#     result = Guest.objects.filter(phone = phone)
#     if not result:
#         return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})
#
#     result = Guest.objects.filter(phone = phone,event_id = event_id)
#     if not result:
#         return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})
#
#     result = Guest.objects.get(event_id = event_id,phone = phone)
#
#     if result.sign:
#         return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
#     else:
#         Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
#         return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
#             'user': result,
#             'guest':guest_data,
#             'sign':str(int(sign_data)+1)
#             })

