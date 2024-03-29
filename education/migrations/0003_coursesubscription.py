# Generated by Django 4.2.5 on 2024-01-10 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0002_alter_course_title_alter_question_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_time', models.DateTimeField(auto_now_add=True, verbose_name='Subscription Time')),
                ('unsub_time', models.DateTimeField(default=None, editable=False, null=True, verbose_name='Unsub Time')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
