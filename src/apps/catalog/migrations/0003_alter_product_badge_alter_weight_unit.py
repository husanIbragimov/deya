from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_category_image_alter_productimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="badge",
            field=models.CharField(
                blank=True,
                choices=[("", ""), ("new", "new"), ("bestseller", "bestseller")],
                default="",
                help_text=" - , new - new, bestseller - bestseller",
                max_length=16,
                verbose_name="badge",
            ),
        ),
        migrations.AlterField(
            model_name="weight",
            name="unit",
            field=models.CharField(
                choices=[("g", "gram"), ("kg", "kilogram")],
                help_text="g - gram, kg - kilogram",
                max_length=2,
                verbose_name="unit",
            ),
        ),
    ]
