from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=40, verbose_name='Question Title', unique=True, db_index=True)
    question_text = models.TextField(verbose_name='Question Text')
    correct_answer = models.TextField(verbose_name='Correct Answer')
    incorrect_answer1 = models.TextField(verbose_name='Incorrect Answer 1', default='Bad answer 1', blank=True)
    incorrect_answer2 = models.TextField(verbose_name='Incorrect Answer 2', default='Bad answer 2', blank=True)
    comment = models.TextField(verbose_name='Comment', default='Your answer is wrong.', blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Time of last update')

    def __str__(self):
        return f'{self.title} (id:{self.id})'


class Test(models.Model):
    title = models.CharField(max_length=40, verbose_name='Test Title', unique=True, db_index=True)
    questions = models.ManyToManyField(Question, verbose_name='Questions in Test')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Time of last update')

    def __str__(self):
        return f'{self.title} (id:{self.id})'


class Course(models.Model):
    title = models.CharField(max_length=40, verbose_name='Course Title', unique=True, db_index=True)
    tests = models.ManyToManyField(Test, verbose_name='Tests in Course')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Time of last update')

    def __str__(self):
        return f'{self.title} (id:{self.id})'