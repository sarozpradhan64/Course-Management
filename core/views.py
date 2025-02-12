from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment


def home(request):
    return render(request, 'pages/home.html')


def courseListView(request):
    courses = Course.objects.filter(is_published=True).values
    context = {'courses': courses}
    return render(request, 'pages/courses.html', context)


def studentListView(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    context = {'course': course, 'enrollments': enrollments}
    return render(request, 'pages/students.html', context)
