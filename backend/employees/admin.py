from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, ClockedSchedule, SolarSchedule
from .models import Employee
from django.urls import reverse
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .tasks import del_payment_info_task

admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)


class EmployeeDraggableAdmin(DraggableMPTTAdmin, UserAdmin):
    model = Employee

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'patronymic',
                           'position', 'employment_date', 'salary', 'total_paid',
                           'head', 'is_staff', 'is_superuser')
                }
         ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name',
                       'last_name', 'patronymic', 'position', 'employment_date',
                       'salary', 'total_paid', 'head', 'is_staff', 'is_superuser')
        }
         ),
    )

    ordering = ('level',)
    list_display = ('tree_actions', 'get_full_name',
                    'position', 'salary', 'total_paid',
                    'link_to_head',
                    )
    list_display_links = ['get_full_name', 'link_to_head']
    list_filter = ('position', 'level')
    actions = ['delete_payment_info']

    def delete_payment_info(self, request, queryset):
        if queryset.count() > 20:
            r = [item for item in queryset.values_list('pk', flat=True)]
            del_payment_info_task.apply_async(kwargs={"queryset": r})
        else:
            queryset.update(total_paid=0)

    def link_to_head(self, obj):
        link = reverse("admin:employees_employee_change", args=[obj.head_id])
        if not obj.head:
            return format_html('<span> No head </span>', link, obj.head)
        return format_html('<a href="{}">{}</a>', link, obj.head)

    delete_payment_info.short_description = 'Delete payment information'
    link_to_head.short_description = 'Head'
    link_to_head.allow_tags = True


admin.site.register(Employee, EmployeeDraggableAdmin)
