# Generated by Django 3.2.3 on 2021-06-29 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0016_alter_transaction_paid_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='paid_sum',
            field=models.FloatField(),
        ),
    ]
