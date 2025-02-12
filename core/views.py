from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Course, Enrollment
from .forms import StudentForm, EnrollmentForm

def home(request):
    return render(request, 'pages/home.html')


def courseListView(request):
    courses = Course.objects.filter(is_published=True).values
    context = {'courses': courses}
    return render(request, 'pages/courses.html', context)


def studentListView(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(
        course=course).select_related('student')

    # enrollment forms
    student_form = StudentForm()
    enrollment_form = EnrollmentForm()
    context = {'course': course, 'enrollments': enrollments,
               'student_form': student_form, 'enrollment_form': enrollment_form
               }
    return render(request, 'pages/students.html', context)


def enrollStudent(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        enrollment_form = EnrollmentForm(request.POST)
        if student_form.is_valid() and enrollment_form.is_valid():
            
            # creating user instance before saving the student
            password = "newpass"
            user = User.objects.create_user(
                username=student_form.cleaned_data['email'],
                email=student_form.cleaned_data['email'],
                password=password
            )
            
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            
            # handling the enrollment
            enrollment = enrollment_form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            
            send_mail(
                'Your have been enrolled!!',
                f'Hi {student.name}, Your have been sucessfully enrolled in the course {enrollment.course.title} Username: {student.email}\nPassword: {password}',
                settings.EMAIL_HOST_USER,
                [student.email],
                fail_silently=False,
            )
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else: 
            return "test"
    else:
        return redirect('home')