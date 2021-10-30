from django.shortcuts import render
from .models import Course
from django.views.generic.list import ListView


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course/list.html'
    context_object_name = 'courses'
