from django.contrib.auth.models import User
from django.db import models


class BaseContent(models.Model):
    """Abstract Class for Questions, Tests, Content and Courses models. Adds Title, DateTime fields and __str__ method"""
    title = models.CharField(max_length=40, unique=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Time of last update')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title} (id:{self.id})'


class Question(BaseContent):
    question_text = models.TextField(verbose_name='Question Text')
    correct_answer = models.TextField(verbose_name='Correct Answer')
    incorrect_answer1 = models.TextField(verbose_name='Incorrect Answer 1', default='Bad answer 1', blank=True)
    incorrect_answer2 = models.TextField(verbose_name='Incorrect Answer 2', default='Bad answer 2', blank=True)
    comment = models.TextField(verbose_name='Comment', default='Your answer is wrong.', blank=True)


class Test(BaseContent):
    questions = models.ManyToManyField(Question, verbose_name='Questions in Test')


class Course(BaseContent):
    tests = models.ManyToManyField(Test, verbose_name='Tests in Course')
    description = models.CharField(max_length=340, verbose_name='Description', blank=True)
    icon = models.ImageField(upload_to='course_icon/', verbose_name='Course Icon', blank=True)

    class Meta:
        ordering = ['id']


def course_directory_path(instance, filename):
    """Function is used to generate the path based on course_name for saving files in different directories"""
    return 'content/{0}/{1}'.format(instance.course.title, filename)


class Content(BaseContent):
    course = models.ForeignKey('Course', on_delete=models.PROTECT, verbose_name='Content in Course')
    file = models.FileField(upload_to=course_directory_path, verbose_name='Content File')


class CourseSubscription(models.Model):
    """Through-Model to connect User and Course. Realize Many-to-Many connection."""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Student')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    sub_time = models.DateTimeField(auto_now_add=True, verbose_name='Subscription Time')
    unsub_time = models.DateTimeField(null=True, default=None, editable=False, verbose_name='Unsub Time')
    active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return f'{self.user}(id:{self.user.id}) - {self.course}(id:{self.course.id})'


class CourseAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Student')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    course_score = models.FloatField(default=0, blank=True, verbose_name='Course Progress (/100)')
    course_passed = models.BooleanField(default=False, verbose_name='Course is done (Yes/No)')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Time of last update')


class TestAttempt(models.Model):
    course_attempt = models.ForeignKey(CourseAttempt, on_delete=models.PROTECT, verbose_name='Course Attempt ID')
    test = models.ForeignKey(Test, on_delete=models.PROTECT, verbose_name='Test Quiz')
    test_score = models.FloatField(default=0, blank=True, verbose_name='Test Progress (/100)')
    test_passed = models.BooleanField(default=False, verbose_name='Test is done (Yes/No)')


class QuestionAttempt(models.Model):
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.PROTECT, verbose_name='Test Attempt ID')
    question = models.ForeignKey(Question, on_delete=models.PROTECT, verbose_name='Question')
    question_passed = models.BooleanField(default=False, verbose_name='Answer is correct (Yes/No)')
