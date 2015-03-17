# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import model_utils.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('payload', jsonfield.fields.JSONField(default=dict)),
                ('success', models.BooleanField(default=False)),
                ('attempt', models.IntegerField(verbose_name='How many times has this been attempted to be delivered')),
                ('hash_value', models.CharField(max_length=255, blank=True)),
                ('notification', models.TextField(verbose_name='Passed back from the Senderable object', blank=True)),
                ('response_message', models.TextField(verbose_name='Whatever is sent back', blank=True)),
                ('response_status', models.IntegerField(verbose_name='HTTP status code', blank=True, null=True)),
                ('response_content_type', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'get_latest_by': 'created',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='WebhookTarget',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('event', models.CharField(choices=[('product.created', 'product.created'), ('product.updated', 'product.updated'), ('product.deleted', 'product.deleted')], max_length=255)),
                ('identifier', models.SlugField(max_length=255, blank=True)),
                ('target_url', models.URLField(max_length=255)),
                ('header_content_type', models.CharField(default='application/json', choices=[('application/json', 'application/json'), ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded')], max_length=255, verbose_name='Header content-type')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='webhooks')),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ['-modified'],
            },
        ),
        migrations.AddField(
            model_name='delivery',
            name='webhook_target',
            field=models.ForeignKey(to='djwebhooks.WebhookTarget'),
        ),
    ]
