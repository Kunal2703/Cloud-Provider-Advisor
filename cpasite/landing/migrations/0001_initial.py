# Generated by Django 4.2 on 2023-04-23 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuthGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
            options={"db_table": "auth_group", "managed": False,},
        ),
        migrations.CreateModel(
            name="AuthGroupPermissions",
            fields=[("id", models.BigAutoField(primary_key=True, serialize=False)),],
            options={"db_table": "auth_group_permissions", "managed": False,},
        ),
        migrations.CreateModel(
            name="AuthPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("codename", models.CharField(max_length=100)),
            ],
            options={"db_table": "auth_permission", "managed": False,},
        ),
        migrations.CreateModel(
            name="AuthUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("is_superuser", models.IntegerField()),
                ("username", models.CharField(max_length=150, unique=True)),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("email", models.CharField(max_length=254)),
                ("is_staff", models.IntegerField()),
                ("is_active", models.IntegerField()),
                ("date_joined", models.DateTimeField()),
            ],
            options={"db_table": "auth_user", "managed": False,},
        ),
        migrations.CreateModel(
            name="AuthUserGroups",
            fields=[("id", models.BigAutoField(primary_key=True, serialize=False)),],
            options={"db_table": "auth_user_groups", "managed": False,},
        ),
        migrations.CreateModel(
            name="AuthUserUserPermissions",
            fields=[("id", models.BigAutoField(primary_key=True, serialize=False)),],
            options={"db_table": "auth_user_user_permissions", "managed": False,},
        ),
        migrations.CreateModel(
            name="Awsprice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "instance_name",
                    models.CharField(
                        blank=True, db_column="Instance_name", max_length=20, null=True
                    ),
                ),
                (
                    "linux_price",
                    models.FloatField(blank=True, db_column="Linux_Price", null=True),
                ),
                (
                    "windows_price",
                    models.FloatField(blank=True, db_column="Windows_Price", null=True),
                ),
                ("vcpu", models.IntegerField(blank=True, db_column="vCPU", null=True)),
                ("memory", models.FloatField(blank=True, null=True)),
                (
                    "storage",
                    models.CharField(
                        blank=True, db_column="Storage", max_length=20, null=True
                    ),
                ),
                (
                    "instance_family",
                    models.CharField(
                        blank=True,
                        db_column="Instance_Family",
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        blank=True, db_column="Region", max_length=40, null=True
                    ),
                ),
            ],
            options={"db_table": "awsprice", "managed": False,},
        ),
        migrations.CreateModel(
            name="Azureprice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "instance_name",
                    models.CharField(
                        blank=True, db_column="Instance_name", max_length=40, null=True
                    ),
                ),
                (
                    "linux_price",
                    models.FloatField(blank=True, db_column="Linux_Price", null=True),
                ),
                (
                    "windows_price",
                    models.FloatField(blank=True, db_column="Windows_Price", null=True),
                ),
                ("vcpu", models.IntegerField(blank=True, db_column="vCPU", null=True)),
                (
                    "memory",
                    models.IntegerField(blank=True, db_column="Memory", null=True),
                ),
                (
                    "storage",
                    models.IntegerField(blank=True, db_column="Storage", null=True),
                ),
                (
                    "instance_family",
                    models.CharField(
                        blank=True,
                        db_column="Instance_Family",
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        blank=True, db_column="Region", max_length=40, null=True
                    ),
                ),
            ],
            options={"db_table": "azureprice", "managed": False,},
        ),
        migrations.CreateModel(
            name="DjangoAdminLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action_time", models.DateTimeField()),
                ("object_id", models.TextField(blank=True, null=True)),
                ("object_repr", models.CharField(max_length=200)),
                ("action_flag", models.PositiveSmallIntegerField()),
                ("change_message", models.TextField()),
            ],
            options={"db_table": "django_admin_log", "managed": False,},
        ),
        migrations.CreateModel(
            name="DjangoContentType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app_label", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
            ],
            options={"db_table": "django_content_type", "managed": False,},
        ),
        migrations.CreateModel(
            name="DjangoMigrations",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("app", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("applied", models.DateTimeField()),
            ],
            options={"db_table": "django_migrations", "managed": False,},
        ),
        migrations.CreateModel(
            name="DjangoSession",
            fields=[
                (
                    "session_key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("session_data", models.TextField()),
                ("expire_date", models.DateTimeField()),
            ],
            options={"db_table": "django_session", "managed": False,},
        ),
        migrations.CreateModel(
            name="Gcpprice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "instance_name",
                    models.CharField(
                        blank=True, db_column="Instance_name", max_length=40, null=True
                    ),
                ),
                (
                    "instance_price",
                    models.FloatField(
                        blank=True, db_column="Instance_Price", null=True
                    ),
                ),
                ("vcpu", models.IntegerField(blank=True, db_column="vCPU", null=True)),
                (
                    "memory",
                    models.IntegerField(blank=True, db_column="Memory", null=True),
                ),
                (
                    "instance_family",
                    models.CharField(
                        blank=True,
                        db_column="Instance_Family",
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        blank=True, db_column="Region", max_length=40, null=True
                    ),
                ),
            ],
            options={"db_table": "gcpprice", "managed": False,},
        ),
    ]
