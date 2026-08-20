from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_post_cover_alter_postblock_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postblock",
            name="type",
            field=models.CharField(
                choices=[("heading", "heading"), ("text", "text"), ("image", "image")],
                help_text="heading - heading, text - text, image - image",
                max_length=16,
                verbose_name="block type",
            ),
        ),
    ]
