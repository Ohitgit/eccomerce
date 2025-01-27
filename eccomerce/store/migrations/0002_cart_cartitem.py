# Generated by Django 5.1.5 on 2025-01-27 13:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, db_index=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('price', models.IntegerField(blank=True, db_index=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='store.cart')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
