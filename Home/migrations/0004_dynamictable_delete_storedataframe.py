# Generated by Django 5.0.1 on 2024-01-09 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_alter_storedataframe_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=100)),
                ('column_type', models.CharField(max_length=100)),
                ('column_value', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='StoreDataframe',
        ),
    ]
