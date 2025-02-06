# Generated by Django 5.1.2 on 2025-01-31 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_users_profileimg"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="profileimg",
            field=models.ImageField(
                blank=True,
                db_column="PROFILEIMG",
                default="media/userimg/blank-profile-picture.png",
                max_length=300,
                null=True,
                upload_to="userimg/",
            ),
        ),
    ]
