import time

from django_seed import Seed
from faker import Faker
from .globals import PATRONYMICS
import random

from employees.models import Employee

PARTONYMIC = []


def create_lead():
    lead = Employee(

        first_name='Петр',
        last_name='Петров',
        patronymic='Петрович',
        position='Генеральный директор',
        employment_date='2000-01-01',
        salary='6000',
        total_paid='0',
        email='lead@mail.ru',
        is_superuser='True',
        is_staff='True'

    )
    lead.set_password('lead')
    lead.save()


def create_employees(count, position, salary, parent_min, parent_max, is_superuser):
    seeder = Seed.seeder()
    fake = Faker('ru_RU')

    with Employee.objects.delay_mptt_updates():
        seeder.add_entity(Employee, count, {
            'first_name': lambda first_name: fake.first_name(),
            'last_name': lambda last_name: fake.last_name(),
            'patronymic': lambda patronymic: PATRONYMICS[random.randint(0, len(PATRONYMICS) - 1)],
            'position': position,
            'employment_date': f'{random.randint(2005, 2021)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
            'salary': lambda x: random.randint(salary - 250, salary + 250),
            'total_paid': lambda x: random.randint(salary, salary * 2),
            'head': lambda x: Employee.objects.get(id=random.randint(parent_min, parent_max)),
            'email': lambda x: seeder.faker.email(),
            'is_superuser': is_superuser,
            'is_staff': 'True',

        })

        seeder.execute()


def del_obj():
    with Employee.objects.disable_mptt_updates():
        objs = Employee.objects.all()
        objs.delete()
    Employee.objects.rebuild()


def run():
    create_lead()
    create_employees(5, 'Заместитель директора', 3500, 1, 1, 'True')
    print('Создано 5 записей заместителей директора')
    create_employees(5, 'Старший менеджер', 2300, 2, 6, 'True')
    print('Создано 10 записей старших менеджеров')
    create_employees(5, 'Менеджер', 1500, 7, 12, 'False')
    print('Создано 15 записей менеджеров')
    create_employees(10, 'Младший менеджер', 1000, 13, 18, 'False')
    print('Создано 40 записей младших менеджеров')
    create_employees(5, 'Стажер', 500, 19, 29, 'False')
    print('Создано 25 записей стажеров')
    Employee.objects.rebuild()
    for emp in Employee.objects.exclude(pk=1):
        emp.set_password('user_pass')
        emp.save()
    print('Установлен грубый пароль : user_pass')
