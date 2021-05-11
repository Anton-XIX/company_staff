from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name',
                  'patronymic', 'position',
                  'employment_date', 'salary',
                  'total_paid', 'head')
