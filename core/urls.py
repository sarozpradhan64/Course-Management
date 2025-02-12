from django.urls import path
from .views import home, courseListView, studentListView, enrollStudent, removeEnrollment
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', home, name='home'),
    path('courses', courseListView, name='course-list'),
    path('courses/<int:course_id>/students',
         studentListView, name='enrolled-students'),
    path('enroll-student', enrollStudent, name='enroll-student'),
    path('remove-enroll/<int:enroll_id>', removeEnrollment, name='remove-enroll'),
] + debug_toolbar_urls()
