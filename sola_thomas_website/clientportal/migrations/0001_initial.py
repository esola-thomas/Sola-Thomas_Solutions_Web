from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('details', models.TextField()),
                ('due_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_link', models.URLField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('date_performed', models.DateField()),
                ('admin_notes', models.TextField(blank=True, help_text='Internal notes visible only to admins', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cost_estimate', models.DecimalField(blank=True, decimal_places=2, help_text='Estimated cost for this work item', max_digits=10, null=True)),
                ('user_approved', models.BooleanField(default=False, help_text='Has the user approved the cost estimate?')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_orders', to='clientportal.invoice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_orders', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='clientportal.workorder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='auth.user')),
            ],
            options={'unique_together': {('user', 'service')},},
        ),
        migrations.CreateModel(
            name='ServiceNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Your message to the admin')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('admin_response', models.TextField(blank=True, null=True)),
                ('response_date', models.DateTimeField(blank=True, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='clientportal.workorder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_notes', to='auth.user')),
            ],
            options={'ordering': ['-created_at'],},
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('requested_date', models.DateField(help_text='Preferred date for service')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_requests', to='auth.user')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_request', to='clientportal.workorder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='auth.user')),
            ],
            options={'ordering': ['-created_at'],},
        ),
    ]
