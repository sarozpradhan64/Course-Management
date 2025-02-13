import secrets
import string
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from .models import Course, Enrollment
from .forms import StudentForm, EnrollmentForm


def check_admin(user):
    return user.is_superuser


def home(request):
    return render(request, 'pages/home.html')


def courseListView(request):
    courses = Course.objects.filter(is_published=True).values
    context = {'courses': courses}
    return render(request, 'pages/courses.html', context)


@user_passes_test(check_admin)
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



def generate_password(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


@user_passes_test(check_admin)
def enrollStudent(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        enrollment_form = EnrollmentForm(request.POST)

        if student_form.is_valid() and enrollment_form.is_valid():
            try:
                # Check if user already exists
                if User.objects.filter(username=student_form.cleaned_data['email']).exists():
                    messages.error(
                        request, "A user with this email already exists.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                
                password = generate_password()
                user = User.objects.create_user(
                    username=student_form.cleaned_data['email'],
                    email=student_form.cleaned_data['email'],
                    password=password
                )

                student = student_form.save(commit=False)
                student.user = user
                student.save()

                enrollment = enrollment_form.save(commit=False)
                enrollment.student = student
                enrollment.save()

                # email
                send_mail(
                    'You have been enrolled!',
                    f'Hi {student.name}, you have been successfully enrolled in the course {enrollment.course.title}.\n'
                    f'Username: {student.email}\nPassword: {password}',
                    settings.EMAIL_HOST_USER,
                    [student.email],
                    fail_silently=False,
                )

                messages.success(request, "Student enrolled successfully!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(
                request, "Invalid form submission. Please check the details and try again.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('home')


@user_passes_test(check_admin)
def removeEnrollment(request, enroll_id):
    enrollment = get_object_or_404(Enrollment, pk=enroll_id)
    enrollment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
