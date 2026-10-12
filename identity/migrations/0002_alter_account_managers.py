import identity.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("identity", "0001_initial")]
    operations = [
        migrations.AlterModelManagers(
            name="account",
            managers=[("objects", identity.models.AccountManager())],
        ),
    ]

