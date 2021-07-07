from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

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

    result=Event.objects.filter(id=id_id)
    if result:
        return JsonResponse({'status':10022,'message':'event id already exists'})

    result=Event.objects.filter(name=name_name)

    if result:
        return JsonResponse ({'status':10023,'message':'event name already exists'})

    if status_status=='':
        status_status=1

    try:
        Event.objects.create(id=id_id,name=name_name,limit=limit_limit,address=address_address,status=int(status_status),start_time=start_time)
     #将数据插入Event表
    except ValidationError as e:
        error='start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status':'10024','message':error})
    return JsonResponse ({'status':200,'message':'add event success'})

#查询发布会接口

def get_event_list(request):

