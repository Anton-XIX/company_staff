from celery import shared_task
from employees.models import Employee


@shared_task
def salary_accounting():
    employees = Employee.objects.all()
    for emp in employees:
        emp.total_paid += emp.salary
        emp.save()


@shared_task
def del_payment_info_task(queryset):
    for emp_id in queryset:
        emp = Employee.objects.get(pk=emp_id)
        emp.total_paid = 0
        emp.save()
