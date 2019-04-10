# Generated by Django 2.1.5 on 2019-04-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20190409_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opioids',
            name='isOpioid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.TextField(choices=[('I', 'Inactive'), ('A', 'Active')], db_index=True, default='A'),
        ),
    ]