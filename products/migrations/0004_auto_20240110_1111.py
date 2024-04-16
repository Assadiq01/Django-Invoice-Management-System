# Generated by Django 3.2.15 on 2024-01-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20240107_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variant',
            old_name='price',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='short_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='balance1',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product',
            name='balance2',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='deposit',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_total',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product',
            name='total',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='variant',
            name='description',
            field=models.TextField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variant',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=12, max_length=12, null=True),
        ),
    ]
