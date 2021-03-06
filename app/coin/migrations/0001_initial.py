# Generated by Django 2.2.4 on 2019-12-10 13:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0104_fix_invalid_attributes_map'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('fixed', 'USD'), ('percentage', '%')], default='fixed', max_length=10)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='product.Category')),
                ('collections', models.ManyToManyField(blank=True, to='product.Collection')),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
            options={
                'permissions': (('manage_discounts', 'Manage sales and vouchers.'),),
            },
        ),
        migrations.CreateModel(
            name='CoinTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='coin.Coin')),
            ],
            options={
                'unique_together': {('language_code', 'coin')},
            },
        ),
    ]
