from django.contrib import admin
from django.urls import reverse
from .views import chart_view
from django.utils.html import format_html
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import Group,User
from chartjs.views.lines import BaseLineChartView

from django.utils.safestring import mark_safe
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from .models import ChapaTransaction

# admin.site.unregister(Group)


import json
from .models import Profile,SentMessage,Created_Group,Contact_List,Contacts,Member,UserProfile,Sender,Receiver,Contactus

# Register your models here.
admin.site.site_header  =  "Debo smsGateway"

admin.site.site_title  =  "Debo  admin site"
admin.site.index_title  =  "Debo sms Admin"

class ChapaTransactionAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'last_name', 'email', 'amount', 'currency', 'status'


admin.site.register(ChapaTransaction, ChapaTransactionAdmin)

class CustomAdminSite(AdminSite):
    def index_view(self, request, extra_context=None):
        # Get the home page URL using reverse function
        home_url = reverse('home')  # Assuming 'home' is the name of your URL pattern for the home page

        # Redirect the user to the home page
        return HttpResponseRedirect(home_url)
admin.site.__class__ = CustomAdminSite
class MemberInline(admin.TabularInline):
    model = Member
    extra = 0

class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

    def get_inline_instances(self, request, obj=None):
        # if obj and not request.user.is_superuser:
        #     return []
        return super().get_inline_instances(request, obj)

class GroupAdmin(MyModelAdmin):
    inlines = [MemberInline]
    list_display = ['group_name', 'company','index_link']
    list_filter = ['group_name']
    search_fields = ['group_name']
    def index_link(self, obj):
        url = reverse('index')  # Replace 'home' with the actual URL name for your home page
        return mark_safe(f'<a href="{url}">Go to Home Page</a>')

    index_link.short_description = "Home"

admin.site.register(Created_Group, GroupAdmin)        
class AdProfile(admin.ModelAdmin):
    list_display= ('bio', 'image', 'name','email')
    list_filter= ('email',)
    search_fields = ['name','email']
class MemberInline(admin.TabularInline):
    model=Member
    extra=0
# class SentMessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'chart_link')
#     # Other admin configurations
    
#     def changelist_view(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         extra_context['chart_link'] = mark_safe(reverse('admin:message_chart'))
#         return super().changelist_view(request, extra_context)
@admin.register(SentMessage)
class SentMessageAdmin(admin.ModelAdmin):
#    class YourChartModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'

class SentMessageChart(BaseLineChartView):
    def get_labels(self):
        return [str(message) for message in SentMessage.objects.all()]

    def get_providers(self):
        return ['message']

    def get_data(self):
        return [list(SentMessage.objects.values_list('message', flat=True))]

    def get_options(self):
        return {
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'beginAtZero': True
                    }
                }]
            }
        }

# @admin.register(SentMessage)
# class SentMessageAdmin(admin.ModelAdmin):
#     list_display = ('sent_at', 'message')
#     readonly_fields = ('view_graph',)

#     def view_graph(self, obj):
#         chart = SentMessageChart()
#         chart.generate()
#         return mark_safe(chart.render_to_html())

#     view_graph.short_description = ' Sent  Message Graph'
# class GroupAdmin(admin.ModelAdmin):
#     inlines=[MemberInline]
#     list_display=['group_name','company']
#     list_filter=['group_name']
#     search_fields=['group_name']
# admin.site.unregister(MyModelAdmin)
# admin.site.unregister(User)
# admin.site.register(Profile,AdProfile)
# admin.site.register(SentMessage)
# admin.site.register(SentMessage,SentMessageAdmin)
# admin.site.register(Group,GroupAdmin)





admin.site.register(Contactus)


# admin.site.register(UserProfile)

# admin.site.register(Sender)
