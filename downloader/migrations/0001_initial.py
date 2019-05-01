from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield

class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL),]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('json_content', jsonfield.JSONField())
            ],
        ),
    ]