from django.contrib import admin
from .models import Quotations, Quotations_details, Quotations_attached_file

admin.site.register(Quotations)
admin.site.register(Quotations_details)
admin.site.register(Quotations_attached_file)
