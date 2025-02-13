from django.contrib import admin
import nested_admin
from .models import *


@admin.register(CourseCategory)
class CouseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'created_at']
    list_filter = ['priority']
    search_fields = ['title']


class CourseVideoAdmin(admin.TabularInline):
    model = CourseVideo
    extra = 1


class CourseDocumentAdmin(admin.TabularInline):
    model = CourseDocument
    extra = 1


@admin.register(Course)
class CouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at']
    list_filter = ['is_published']
    search_fields = ['title']
    inlines = [CourseVideoAdmin, CourseDocumentAdmin]


class MCQChoiceAdmin(nested_admin.NestedTabularInline):
    model = MCQChoice
    max_num=4
    min_num=4


class MCQQuestionAdmin(nested_admin.NestedTabularInline):
    model = MCQQuestion
    extra = 1
    inlines = [MCQChoiceAdmin]


@admin.register(MCQQuiz)
class MCQQuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', 'course']
    list_filter = ['course']
    search_fields = ['course', 'title']
    inlines = [MCQQuestionAdmin]
    
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['email', 'name']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course']
    list_link = ['student']
    search_fields = ['course', 'student']