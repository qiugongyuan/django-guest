from django.http import JsonResponse
from sign.models import Event_new
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from sign.models import Guest_new
from django.db.utils import IntegrityError
import time

#添加发布会接口

def add_event(request):
    id_id=request.POST.get('id','')
    name_name=request.POST.get('name','')
    limit_limit=request.POST.get('limit','')
    status_status=request.POST.get('status','')
    address_address=request.POST.get('address','')
    start_time=request.POST.get('start_time','')

    if id_id=='' or name_name=='' or limit_limit=='' or address_address=='' or start_time=='':
        return JsonResponse({'status':10021,'message':'parameter error'})

    result=Event_new.objects.filter(id=id_id)
    if result:
        return JsonResponse({'status':10022,'message':'event id already exists'})

    result=Event_new.objects.filter(name=name_name)

    if result:
        return JsonResponse ({'status':10023,'message':'event name already exists'})

    if status_status=='':
        status_status=1

    try:
        Event_new.objects.create(id=id_id,name=name_name,limit=limit_limit,address=address_address,status=int(status_status),start_time=start_time)
     #将数据插入Event表
    except ValidationError as e:
        error='start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status':10024,'message':error})
    return JsonResponse ({'status':200,'message':'add event success'})

#查询发布会接口

def get_event_list(request):
    #通过get请求发布会id和name
    id=request.GET.get("id","")
    name=request.GET.get("name","")

    if id=='' and name=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    #id和name同时为空，返回错误码和错误提示
    if id!='':
        event={}
        try:
            result=Event_new.objects.get(id=id)
        except ObjectDoesNotExist:
         return JsonResponse({'status':10022,'message':'query result is empty'})
        else:
            event['id']=result.id
            event['name']=result.name
            event['limit']=result.limit
            event['status']=result.status
            event['address']=result.address
            event['start_time']=result.start_time
            return JsonResponse ({'status':200,'message':'success','data':event})
    #如果id不为空，优先使用id查询，因为id具有唯一性，查询结果只有一条。
    #将查询结果以字典的形式存放到定义的event中，并将event作为接口返回字典中data对应的值
    if name!='':
        datas=[]
        results=Event_new.objects.filter(name__icontains=name)
        if results:
            for r in results:
                event={}
                event['id']=r.id
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse ({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'query result is empty'})
    #用name查询数据可能有多条
    # 将查询的数据放到event字典中；把event字典放到datas数组中；将整个datas数组作为接口返回字典中data对应的值

#添加嘉宾接口
def add_guest(request):
    id=request.POST.get('event_id','')
    realname=request.POST.get('realname','')
    phone=request.POST.get('phone','')
    Email=request.POST.get('Email','')

    if id=='' or realname=='' or phone=='':
        return JsonResponse({'status':10021,'message':'parameter error'})

    # result=Event.objects.get(id=id)
    # if not result:
    #     return JsonResponse({'status':10022,'message':'event id null'})
    if id != '':
        try:
            Event_new.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'event id null'})


    result=Event_new.objects.get(id=id).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status is not available'})

    event_limit=Event_new.objects.get(id=id).limit #发布会限制人数
    guest_limit=Guest_new.objects.filter(event_id=id)#发布会已经添加的嘉宾数

    if len(guest_limit)>=event_limit:
        return JsonResponse({"status":10024,'message':'event number is full'})

    event_time=Event_new.objects.get(id=id).start_time
    etime=str(event_time).split("+")[0]
    timeArray=time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    e_time=int(time.mktime(timeArray))

    now_time=str(time.time())
    ntime=now_time.split(".")[0]
    n_time=int(ntime)

    if n_time>=e_time:
        return JsonResponse({'status':10025,'message':'event has started'})
    try:
        Guest_new.objects.create(realname=realname,phone=int(phone),Email=Email,sign=0,event_id=int(id))
    except IntegrityError:
        return JsonResponse({'status':10026,'message':'The event guest phone number repeat'})
    # //设计数据库时，没有实现该功能

    return JsonResponse({'status':200,'message':'add guest success'})


#查询嘉宾接口
def get_guest_list(request):
    id=request.GET.get("id",'')
    phone=request.GET.get('phone','')

    if  id =='':
        return JsonResponse ({"status":10021,'message':'id connot be empty'})

    if id!='' and phone=='':
        datas=[]
        results=Guest_new.objects.filter(event_id=id)
        if results:
            for i in results:
                guest={}
                guest['realname']=i.realname
                guest['phone']=i.phone
                guest['Email']=i.Email
                guest['sign']=i.sign
                datas.append(guest)
            return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'query result is empty'})

    if id!='' and phone!='':
            das=[]
            results=Guest_new.objects.filter(phone=phone,event_id=id)
            if results:
                for s in results:
                     guest={}
                     guest['realname']=s.realname
                     guest['phone']=s.phone
                     guest['sign']=s.sign
                     guest['Email']=s.Email
                     das.append(guest)
                return JsonResponse({'status':200,'message':'success','data':das})
            else:
                return JsonResponse({'status':10022,'message':'query result is empty'})

#发布会签到接口
def user_sign(request):
    id=request.POST.get('id','')
    phone=request.POST.get('phone','')

    if id=='' or phone=='':
        return JsonResponse({'status':10021,'message':'parameter error'})

    result=Event_new.objects.filter(id=id)
    if not result:
        return JsonResponse({'status':10022,'message':'event id null'})

    result=Event_new.objects.get(id=id).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status is not available'})



    event_time=Event_new.objects.get(id=id).start_time
    etime=str(event_time).split("+")[0]
    timeArray=time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    e_time=int(time.mktime(timeArray))

    now_time=str(time.time())
    ntime=now_time.split(".")[0]
    n_time=int(ntime)

    if n_time>=e_time:
        return JsonResponse({'status':10024,'message':'event has started'})

    result=Guest_new.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status':10025,'message':'user phone null'})

    result=Guest_new.objects.filter(event_id=id,phone=phone)
    if not result:
        return JsonResponse({'status':10026,'message':'user did not pacticipate in the conference'})
    result=Guest_new.objects.get(event_id=id,phone=phone).sign
    if result:
        return JsonResponse({'status':10027,'message':"user has sign in"})
    else:
        Guest_new.objects.filter(event_id=id,phone=phone).update(sign='1')
        return JsonResponse({'status':200,'message':'sign success'})