from django.contrib import admin
from schedule.forms import RuleForm
from schedule.models import Calendar, Event, CalendarRelation, Rule

class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

class RuleAdmin(admin.ModelAdmin):
    form = RuleForm

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'location') 
    search_fields = ('title', 'location', 'description')
    date_hierarchy = "created_on"
    ordering = ("-start", )

admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(CalendarRelation)
