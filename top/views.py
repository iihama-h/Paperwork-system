from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class TopView(LoginRequiredMixin, generic.TemplateView):
    template_name = "top.html"
