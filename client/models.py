from django.db import models


class Clients_manager(models.Manager):
    def check_enabled(self):
        return self.filter(is_active=True)


class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    name_kana = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    capital = models.IntegerField(blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fax_number = models.CharField(max_length=255, blank=True, null=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    revenue = models.IntegerField(blank=True, null=True)
    profit = models.IntegerField(blank=True, null=True)
    number_of_employees = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "clients"
        ordering = ['-updated_datetime']

    objects = Clients_manager()
