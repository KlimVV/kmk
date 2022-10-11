# Generated by Django 4.1.1 on 2022-10-04 19:19

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_articlepage_tag_author_articlepagetag_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlepage",
            name="annotation",
            field=wagtail.fields.RichTextField(blank=True, verbose_name="Анотація"),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="event",
            field=models.CharField(
                blank=True,
                max_length=1024,
                null=True,
                verbose_name="Захід (конференція, видання тощо)",
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="issue",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="Де опубліковано"
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="pubdate",
            field=models.DateField(
                blank=True, null=True, verbose_name="Дата публікації"
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="pubtitle",
            field=models.CharField(
                max_length=1024, verbose_name="Повна назва публікації"
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="team",
            field=models.CharField(max_length=1024, verbose_name="Усі автори"),
        ),
        migrations.AlterField(
            model_name="author",
            name="fname",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="По батькові"
            ),
        ),
        migrations.AlterField(
            model_name="author",
            name="name",
            field=models.CharField(max_length=25, verbose_name="Ім'я"),
        ),
        migrations.AlterField(
            model_name="author",
            name="surname",
            field=models.CharField(max_length=25, verbose_name="Прізвище"),
        ),
    ]
