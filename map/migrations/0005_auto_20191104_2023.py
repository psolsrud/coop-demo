# Generated by Django 2.0.7 on 2019-11-04 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20191101_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datadetailmodel',
            old_name='deployment_date',
            new_name='a_1',
        ),
        migrations.RenameField(
            model_name='datadetailmodel',
            old_name='equipment',
            new_name='a_2',
        ),
        migrations.RenameField(
            model_name='datadetailmodel',
            old_name='services',
            new_name='b_1',
        ),
        migrations.RenameField(
            model_name='datadetailmodel',
            old_name='speed',
            new_name='b_2',
        ),
        migrations.AddField(
            model_name='datadetailmodel',
            name='c_1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='datadetailmodel',
            name='c_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='datadetailmodel',
            name='d_1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='datadetailmodel',
            name='d_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='datadetailmodel',
            name='e_1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='datadetailmodel',
            name='e_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
