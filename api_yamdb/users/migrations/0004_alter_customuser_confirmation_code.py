# Generated by Django 3.2 on 2024-07-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(blank=True, default=None, max_length=6, null=True, verbose_name='Код подтверждения'),
        ),
    ]
