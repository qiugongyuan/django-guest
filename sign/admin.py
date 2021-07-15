from django.contrib import admin
from sign.models import Event_new,Guest_new
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['id','name','status','address','start_time']
    search_fields = ['name']#搜索栏
    list_filter = ['status']#过滤栏
class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname','phone','Email','sign','create_time','event']
    search_fields = ['realname','phone']  # 搜索栏
    list_filter = ['sign']  # 过滤栏
admin.site.register(Event_new,EventAdmin)
admin.site.register(Guest_new,GuestAdmin)