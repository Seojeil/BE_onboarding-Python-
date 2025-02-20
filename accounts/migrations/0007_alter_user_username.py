# Generated by Django 5.1.3 on 2024-11-09 06:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="사용자 이름에는 알파벳 대소문자, 한글, 공백 및 특수문자(@, ., /, +, -, _)만 포함 가능합니다.",
                        regex="^[a-zA-Z0-9@./+\\-_ ]+$",
                    )
                ],
                verbose_name="username",
            ),
        ),
    ]
