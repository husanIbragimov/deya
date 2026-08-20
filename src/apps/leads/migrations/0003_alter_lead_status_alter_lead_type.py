from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0002_alter_lead_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lead",
            name="status",
            field=models.CharField(
                choices=[("new", "new"), ("in_progress", "In progress"), ("done", "done")],
                db_index=True,
                default="new",
                help_text="new - new, in_progress - In progress, done - done",
                max_length=16,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="lead",
            name="type",
            field=models.CharField(
                choices=[("partner", "partner"), ("sales", "sales"), ("contact", "contact")],
                db_index=True,
                help_text="partner - partner, sales - sales, contact - contact",
                max_length=16,
                verbose_name="lead type",
            ),
        ),
    ]
