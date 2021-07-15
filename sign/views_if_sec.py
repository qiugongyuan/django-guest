import hashlib
import time
from urllib import request

from django.contrib import auth as django_auth
import base64
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse


from sign.models import Event_new

#查询发布会接口---增加用户认证
def user_auth(request):
    #user_auth函数的处理过程主要是提取出用户认证数据并判断其正确性
    get_http_auth=request.META.get('HTTP_AUTHORIZATION',b'')
    auth=get_http_auth.split()
    try:
        auth_parts=base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return "null"
    username,password = auth_parts[0],auth_parts[2]
    user=django_auth.authenticate(username=username,password=password)
    if user is not None:
        django_auth.login(request,user)
        return "success"
    else:
        return "fail"



#查询发布会接口

def get_sec_event_list(request):
    auth_result=user_auth(request)
    if auth_result=='null':
       return JsonResponse({'status':10011,'message':'user auth null'})
    if auth_result=='fail':
        return JsonResponse({'status':10012,'message':'user auth fail'})
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
    # 将查询的数据放到event字典中；把event字典放到datas数组中；将整个datas数组作为接口返回字典中data对应的


#接口签名

def user_sign(request):
        if request.method=='POST':
            client_time=request.POST.get('time','')
            client_sign=request.POST.get('sign','')
        else:
            return "error"

        if client_time=='' or client_sign=='':
            return 'sign null'

        #服务器时间
        now_time=time.time()
        server_time=str(now_time).split('.')[0]
        #获取时间差
        time_difference=int(server_time)-int(client_time)
        if time_difference>=60:
            return 'time out'

        #签名检查
        md5=hashlib.md5()
        sign_str=client_time+"&Guest-Bugmaster"
        sign_bytes_utf8=sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        server_sign=md5.hexdigest()

        if server_sign!=client_sign:
            return "sign fail"
        else:
            return "sign success"

    #添加发布会接口--增加签名+时间戳
def add_sec_event(request):
        sign_result=user_sign(request)
        if sign_result=='error':
            return JsonResponse({'status':10011,'message':'request error'})
        elif sign_result=='sign null':
            return JsonResponse({'status':10012,'message':'user sign null'})
        elif sign_result=='timeout':
            return JsonResponse({'status':10013,'message':'user sign timeout'})
        elif sign_result=='sign fail':
            return JsonResponse({'status':10014,'message':'user sign error'})

        id_id = request.POST.get('id', '')
        name_name = request.POST.get('name', '')
        limit_limit = request.POST.get('limit', '')
        status_status = request.POST.get('status', '')
        address_address = request.POST.get('address', '')
        start_time = request.POST.get('start_time', '')

        if id_id == '' or name_name == '' or limit_limit == '' or address_address == '' or start_time == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        result = Event_new.objects.filter(id=id_id)
        if result:
            return JsonResponse({'status': 10022, 'message': 'event id already exists'})

        result = Event_new.objects.filter(name=name_name)

        if result:
            return JsonResponse({'status': 10023, 'message': 'event name already exists'})

        if status_status == '':
            status_status = 1

        try:
            Event_new.objects.create(id=id_id, name=name_name, limit=limit_limit, address=address_address,
                                     status=int(status_status), start_time=start_time)
        # 将数据插入Event表
        except ValidationError as e:
            error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
            return JsonResponse({'status': 10024, 'message': error})
        return JsonResponse({'status': 200, 'message': 'add event success'})


