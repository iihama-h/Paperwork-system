import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import ClientForm, SearchForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Clients
from django.db.models import Q

logger = logging.getLogger(__name__)


class RegistrationView(LoginRequiredMixin, generic.CreateView):
    model = Clients
    template_name = "client_registration.html"
    form_class = ClientForm
    success_url = reverse_lazy('client:registration')

    def form_valid(self, form):
        model_instance = form.save()
        logger.info(
            'Client client_id:{} has been created by Users.id:{}'.format(
                model_instance.client_id,
                self.request.user.id))
        messages.success(self.request, '登録が完了しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(
            'Client could not be registered by Users.id:{} \r\n{}'.format(
                self.request.user.id,
                self.request.POST))
        messages.error(self.request, '登録ができませんでした。')
        return super().form_invalid(form)


class ListView(LoginRequiredMixin, generic.ListView):
    model = Clients
    template_name = 'client_list.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        client_form_value = [
            self.request.POST.get('name', None),
            self.request.POST.get('name_kana', None)
        ]
        request.session['client_form_value'] = client_form_value

        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = ''
        name_kana = ''

        if 'client_form_value' in self.request.session:
            client_form_value = self.request.session['client_form_value']
            name = client_form_value[0]
            name_kana = client_form_value[1]

        default_data = {'name': name, 'name_kana': name_kana, }
        search_form = SearchForm(initial=default_data)  # 検索フォーム
        context['search_form'] = search_form

        return context

    def get_queryset(self):
        if 'client_form_value' in self.request.session:
            client_form_value = self.request.session['client_form_value']
            name = client_form_value[0]
            name_kana = client_form_value[1]

            condition_name = Q()
            condition_name_kana = Q()

            if len(name) != 0:
                condition_name = Q(name__icontains=name)
            if len(name_kana) != 0:
                condition_name_kana = Q(name_kana__icontains=name_kana)
            return Clients.objects.select_related().filter(
                condition_name & condition_name_kana & Q(is_active=True))
        else:
            return Clients.objects.check_enabled()


class ReferenceView(LoginRequiredMixin, generic.UpdateView):
    model = Clients
    template_name = 'client_reference.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy('client:reference', kwargs={
                            'pk': self.kwargs['pk']})

    def form_valid(self, form):
        model_instance = form.save()
        logger.info(
            'Client client_id:{} has been updated by Users.id:{}'.format(
                model_instance.client_id,
                self.request.user.id))
        messages.success(self.request, '更新が完了しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(
            'Client could not be updated by Users.id:{} \r\n{}'.format(
                self.request.user.id,
                self.request.POST))
        messages.error(self.request, '更新ができませんでした。')
        return super().form_invalid(form)


class DeleteView(LoginRequiredMixin, generic.UpdateView):
    model = Clients
    fields = ('is_active',)
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client:list')

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.is_active = False
        model_instance.save()
        logger.info(
            'Client client_id:{} has been deleted by Users.id:{}'.format(
                model_instance.client_id,
                self.request.user.id))
        messages.success(self.request, '削除が完了しました。')
        return super().form_valid(form)
