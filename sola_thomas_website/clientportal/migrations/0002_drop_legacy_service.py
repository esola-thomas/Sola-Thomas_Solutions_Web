from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("clientportal", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS clientportal_service CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
