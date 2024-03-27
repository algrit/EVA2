# Generated by Django 4.2.5 on 2024-01-25 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0008_coursesubscription_course_passed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testattempt',
            name='active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='testattempt',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Student'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testattempt',
            name='test_passed',
            field=models.BooleanField(default=False, verbose_name='Test is passed (Yes/No)'),
        ),
    ]
