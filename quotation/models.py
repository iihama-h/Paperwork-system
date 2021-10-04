from django.db import models
from client.models import Clients
from accounts.models import Users
from paperwork_system.constant_values import QUOTATION＿EXPIRY


class Quotations_manager(models.Manager):
    def check_enabled(self):
        return self.filter(is_active=True)


class Quotations_details_manager(models.Manager):
    def check_enabled(self):
        return self.filter(is_active=True)


class Quotations_attached_file_manager(models.Manager):
    def check_enabled(self):
        return self.filter(is_active=True)


class Quotations(models.Model):
    quotation_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(
        Clients,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column='client_id')
    username = models.ForeignKey(
        Users,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column='username')
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    expiry = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=QUOTATION＿EXPIRY)
    recipient = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    delivery_time = models.CharField(max_length=255, blank=True, null=True)
    delivery_location = models.CharField(max_length=255, blank=True, null=True)
    delivery_method = models.CharField(max_length=255, blank=True, null=True)
    payment_condition = models.CharField(max_length=255, blank=True, null=True)
    consumption_tax = models.IntegerField(default=0, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.quotation_id)

    class Meta:
        verbose_name_plural = "quotations"
        ordering = ['-updated_datetime']

    objects = Quotations_manager()


class Quotations_details(models.Model):
    quotation_id = models.ForeignKey(
        Quotations,
        on_delete=models.CASCADE,
        db_column='quotation_id')
    item_id = models.CharField(primary_key=True, max_length=255)
    merchandise = models.CharField(max_length=255, blank=True, null=True)
    merchandise_description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=255, blank=True, null=True)
    sales_unit_price = models.IntegerField(default=0)
    purchase_unit_price = models.IntegerField(default=0)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.item_id)

    class Meta:
        verbose_name_plural = "quotations_details"
        ordering = ['order']

    objects = Quotations_details_manager()


class Quotations_attached_file(models.Model):
    quotation_id = models.OneToOneField(
        Quotations,
        on_delete=models.CASCADE,
        db_column='quotation_id',
        primary_key=True)
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name_plural = "quotations_attached_file"

    objects = Quotations_attached_file_manager()
