from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator 



class CourseCategory(models.Model):
    title = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_categories"
        ordering = ['priority']
        verbose_name_plural = 'Course Categories'

    def __str__(self):
        return self.title


class Course(models.Model):
    category = models.ForeignKey(
        CourseCategory, related_name="courses", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "courses"
        ordering = ['title']

    def __str__(self):
        return self.title


# File path to upload the video and documents
def file_path(instance, filename):
    return f'course_{instance.course.id}/{filename}'


def validate_file_size_video(value):
    filesize = value.size
    if filesize > 52428800:  # 50MB
        raise ValidationError("Maximum file size is 50MB")

class CourseVideo(models.Model):
    course = models.ForeignKey(
        Course, related_name="videos", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=file_path, validators=[validate_file_size_video, FileExtensionValidator(['mp4'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_videos"

    def __str__(self):
        return self.title


def validate_file_size_document(value):
    filesize = value.size
    if filesize > 10485760:  # 10MB
        raise ValidationError("Maximum file size is 10MB")

class CourseDocument(models.Model):
    course = models.ForeignKey(
        Course, related_name="documents", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=file_path, validators=[validate_file_size_document, FileExtensionValidator(['pdf'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_documents"

    def __str__(self):
        return self.title


class MCQQuiz(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mcq_quizzes"
        verbose_name_plural = 'MCQ Quizzes'


class MCQQuestion(models.Model):
    quiz = models.ForeignKey(
        MCQQuiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()

    class Meta:
        db_table = "mcq_questions"


class MCQChoice(models.Model):
    question = models.ForeignKey(
        MCQQuestion, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = "mcq_choices"

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "students"

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "enrollments"
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} enrolled to {self.course.title}"
