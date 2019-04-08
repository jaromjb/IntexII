# Generated by Django 2.1.5 on 2019-04-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20190408_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.TextField(choices=[('I', 'Inactive'), ('A', 'Active')], db_index=True, default='A'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='doctorID',
            field=models.IntegerField(),
        ),
    ]