from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.IntegerField(
                choices=[(0, "Admin"), (1, "User")],
                default=1,
                help_text="0 - Admin, 1 - User",
            ),
        ),
    ]
