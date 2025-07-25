# Generated manually to fix email field length

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ] 