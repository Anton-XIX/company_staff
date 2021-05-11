
from django.urls import path

from .views import EmployeeListCreateView, EmployeeRetriveView
urlpatterns = [

    path("employee/", EmployeeListCreateView.as_view()),
    path("employee/me", EmployeeRetriveView.as_view()),

]
