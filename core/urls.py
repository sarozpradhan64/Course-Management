from django.urls import path
from .views import home, courseListView, studentListView
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', home, name='home'),
    path('courses', courseListView, name='course-list'),
    path('courses/<int:course_id>/students',
         studentListView, name='enrolled-students')
] + debug_toolbar_urls()
