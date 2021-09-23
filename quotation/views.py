import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import QuotationsForm, Quotations_details_formSet, Quotations_attached_file_Form, SearchForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Quotations, Quotations_details, Quotations_attached_file, Clients
from django.db import transaction
from django.db.models import Q
from paperwork_system.lib.models_module import make_composite_key
from .lib.views_module import isnot_detail_empty
from django.http import FileResponse
from django.conf import settings
from .lib.quotation_excel.create_excel import create_excel
from django.shortcuts import redirect
from quotation.lib import calculation_module

logger = logging.getLogger(__name__)


class RegistrationView(LoginRequiredMixin, generic.CreateView):
    model = Quotations
    template_name = "quotation_registration.html"
    form_class = QuotationsForm
    form_class_Quotations_details = Quotations_details_formSet
    form_class_Quotations_attached_file = Quotations_attached_file_Form
    success_url = reverse_lazy('quotation:registration')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Quotations_details_form = self.form_class_Quotations_details(
            self.request.POST or None, instance=self.object)
        context.update({'Quotations_details_form': Quotations_details_form})
        Quotations_attached_file_form = self.form_class_Quotations_attached_file(
            self.request.POST or None, instance=self.object)
        context.update(
            {'Quotations_attached_file_form': Quotations_attached_file_form})
        clients_queryset = Clients.objects.filter(is_active=True)
        context.update({'clients': clients_queryset})  # 顧客フィールドのサジェスト機能用
        return context

    def form_valid(self, form):
        quotation = form.save(commit=False)
        quotation.username = self.request.user
        context = self.get_context_data()
        details_formset = context['Quotations_details_form']
        attached_file_form = context['Quotations_attached_file_form']

        if not Clients.objects.get(
                pk=self.request.POST.get('client_id')).is_active:
            messages.error(self.request, '顧客が存在しませんでした。')
            return self.form_invalid(form)

        if details_formset.is_valid() and attached_file_form.is_valid(
        ):
            with transaction.atomic():
                quotation.save()
                unit_amount_list = []

                i = 0
                for details_form in details_formset:
                    if isnot_detail_empty(self.request.POST, i, 'merchandise', '')\
                            or isnot_detail_empty(self.request.POST, i, 'merchandise_description', '')\
                            or isnot_detail_empty(self.request.POST, i, 'quantity', '0')\
                            or isnot_detail_empty(self.request.POST, i, 'unit', '')\
                            or isnot_detail_empty(self.request.POST, i, 'sales_unit_price', '0')\
                            or isnot_detail_empty(self.request.POST, i, 'purchase_unit_price', '0'):  # 空のdetailがリクエストされた際は処理を行わない
                        quotation_detail = details_form.save(commit=False)
                        quotation_detail.item_id = make_composite_key(
                            quotation.quotation_id, Quotations_details)
                        quotation_detail.quotation_id = quotation
                        quotation_detail.is_active = True  # formsetの場合はModelのdefault値が　適応されないため明示的に値を設定
                        unit_amount_list.append(
                            quotation_detail.sales_unit_price *
                            quotation_detail.quantity)
                        Quotations_details_model_instance = quotation_detail.save()
                    i += 1

                quotation.consumption_tax = calculation_module.consumption_tax(
                    unit_amount_list)
                quotation.save()

                if self.request.POST.get(
                        'file') != '':  # 空のfailがリクエストされた際は処理を行わない
                    Quotations_attached_file.objects.create(
                        quotation_id=quotation,
                        file=self.request.FILES['file'],
                    )

            logger.info(
                'Quotation quotation_id:{} has been created by Users.id:{}'.format(
                    quotation.quotation_id,
                    self.request.user.id))
            messages.success(self.request, '登録が完了しました。')
        else:
            self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        try:
            if not Clients.objects.filter(
                    pk=self.request.POST.get('client_id')).exists():
                messages.error(self.request, '顧客が存在しませんでした。')
        except ValueError:
            messages.error(self.request, '顧客フィールドには顧客IDを入力してください。')

        logger.error(
            'Quotation could not be registered by Users.id:{} \r\n{}'.format(
                self.request.user.id,
                self.request.POST))
        messages.error(self.request, '登録ができませんでした。')

        return super().form_invalid(form)


class ListView(LoginRequiredMixin, generic.ListView):
    model = Quotations
    template_name = 'quotation_list.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        quotation_form_value = [
            self.request.POST.get('name', None),
            self.request.POST.get('username', None),
            self.request.POST.get('updated_datetime', None),
            self.request.POST.get('title', None)
        ]
        request.session['quotation_form_value'] = quotation_form_value

        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = ''
        username = ''
        updated_datetime = ''
        title = ''

        if 'quotation_form_value' in self.request.session:
            quotation_form_value = self.request.session['quotation_form_value']
            name = quotation_form_value[0]
            username = quotation_form_value[1]
            updated_datetime = quotation_form_value[2]
            title = quotation_form_value[3]

        default_data = {
            'name': name,
            'username': username,
            'updated_datetime': updated_datetime,
            'title': title,
        }
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form

        return context

    def get_queryset(self):
        if 'quotation_form_value' in self.request.session:
            quotation_form_value = self.request.session['quotation_form_value']
            client_id_list = list(
                Clients.objects.select_related().filter(
                    name__icontains=quotation_form_value[0]).values_list(
                    'pk', flat=True))
            username = quotation_form_value[1]
            updated_datetime = quotation_form_value[2]
            title = quotation_form_value[3]

            condition_client_id = Q()
            condition_username = Q()
            condition_updated_datetime = Q()
            condition_title = Q()

            if condition_client_id is not None and len(
                    client_id_list) == 0:  # 検索条件の顧客名が入力されているが、filterの結果が空であった場合
                return Quotations.objects.none()
            if len(client_id_list) != 0:
                for client_id in client_id_list:
                    condition_client_id.add(
                        Q(client_id__exact=client_id), Q.OR)
            if len(username) != 0:
                condition_username = Q(username__username__icontains=username)
            if len(updated_datetime) != 0:
                condition_updated_datetime = Q(
                    updated_datetime__icontains=updated_datetime)
            if len(title) != 0:
                condition_title = Q(title__icontains=title)
            return Quotations.objects.select_related().filter(condition_client_id &
                                                              condition_username & condition_updated_datetime & condition_title)
        else:
            return Quotations.objects.check_enabled()


class ReferenceView(LoginRequiredMixin, generic.UpdateView):
    model = Quotations
    template_name = "quotation_reference.html"
    form_class = QuotationsForm
    form_class_Quotations_details = Quotations_details_formSet
    form_class_Quotations_attached_file = Quotations_attached_file_Form

    def get_success_url(self):
        return reverse_lazy('quotation:reference', kwargs={
                            'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        Quotations_details_form = self.form_class_Quotations_details(
            self.request.POST or None, instance=self.object)
        context.update({'Quotations_details_form': Quotations_details_form})

        Quotations_details_queryset = Quotations_details.objects.filter(
            quotation_id=self.kwargs['pk'])
        consumption_tax = Quotations.objects.get(
            quotation_id=self.kwargs['pk']).consumption_tax
        sales_unit_price_list = []
        purchase_unit_price_list = []
        for Quotations_details_unit in Quotations_details_queryset:
            sales_unit_price_list.append(
                Quotations_details_unit.sales_unit_price *
                Quotations_details_unit.quantity)
            purchase_unit_price_list.append(
                Quotations_details_unit.purchase_unit_price *
                Quotations_details_unit.quantity)
        context.update({'sub_total': "{:,}".format(
            calculation_module.sub_total(sales_unit_price_list))})
        context.update({'consumption_tax': "{:,}".format(consumption_tax)})
        context.update({'total_amount': "{:,}".format(
            calculation_module.total_amount(sales_unit_price_list))})
        context.update({'gross_profit': "{:,}".format(calculation_module.gross_profit(
            sales_unit_price_list, purchase_unit_price_list))})
        context.update({'gross_margin': calculation_module.gross_margin(
            sales_unit_price_list, purchase_unit_price_list)})

        attached_file_querySet = Quotations_attached_file.objects.filter(
            quotation_id=self.kwargs['pk'])
        if attached_file_querySet.first() is None:
            Quotations_attached_file_form = self.form_class_Quotations_attached_file(
                self.request.POST or None, instance=self.object)
            context.update(
                {'Quotations_attached_file_form_type': 'attached_file_registration'})
        else:
            Quotations_attached_file_form = attached_file_querySet
            context.update(
                {'Quotations_attached_file_form_type': 'attached_file_reference'})
        context.update(
            {'Quotations_attached_file_form': Quotations_attached_file_form})

        clients_queryset = Clients.objects.filter(is_active=True)
        context.update({'clients': clients_queryset})  # 顧客フィールドのサジェスト機能用

        initial_display_clients_queryset = Clients.objects.all()
        # 顧客フィールドの初期表示用
        context.update(
            {'initial_display_clients': initial_display_clients_queryset})

        return context

    def form_valid(self, form):
        quotation = form.save(commit=False)
        context = self.get_context_data()
        details_formset = context['Quotations_details_form']
        attached_file_form = context['Quotations_attached_file_form']

        attached_file_form_type = context['Quotations_attached_file_form_type']
        attached_file_is_valid = False
        # attached_file_formに格納されている種別が、登録前のQuotations_attached_file_Formの場合
        if attached_file_form_type == 'attached_file_registration':
            if attached_file_form.is_valid():
                attached_file_is_valid = True
        else:  # attached_file_formに格納されている種別が、登録後のファイル(QuerySet)の場合
            attached_file_is_valid = True

        if not Clients.objects.get(
                pk=self.request.POST.get('client_id')).is_active:
            messages.error(self.request, '顧客が存在しませんでした。')
            return self.form_invalid(form)

        if details_formset.is_valid() and attached_file_is_valid:
            with transaction.atomic():
                quotation.save()
                unit_amount_list = []

                Quotations_details.objects.filter(
                    quotation_id=quotation.quotation_id).delete()
                i = 0
                for details_form in details_formset:
                    if isnot_detail_empty(self.request.POST, i, 'merchandise', '')\
                            or isnot_detail_empty(self.request.POST, i, 'merchandise_description', '')\
                            or isnot_detail_empty(self.request.POST, i, 'quantity', '0')\
                            or isnot_detail_empty(self.request.POST, i, 'unit', '')\
                            or isnot_detail_empty(self.request.POST, i, 'sales_unit_price', '0')\
                            or isnot_detail_empty(self.request.POST, i, 'purchase_unit_price', '0'):  # 空のdetailがリクエストされた際は処理を行わない
                        quotation_detail = details_form.save(commit=False)
                        quotation_detail.item_id = make_composite_key(
                            quotation.quotation_id, Quotations_details)
                        quotation_detail.quotation_id = quotation
                        quotation_detail.is_active = True  # formsetの場合はModelのdefault値が　適応されないため明示的に値を設定
                        unit_amount_list.append(
                            quotation_detail.sales_unit_price *
                            quotation_detail.quantity)
                        Quotations_details_model_instance = quotation_detail.save()
                    i += 1

                quotation.consumption_tax = calculation_module.consumption_tax(
                    unit_amount_list)
                quotation.save()

                if Quotations_attached_file.objects.filter(quotation_id=self.kwargs['pk']).first(
                ) is None:  # Quotations_attached_fileが登録されていない場合は処理を行わない
                    if self.request.POST.get(
                            'file') != '':  # 空のfailがリクエストされた際は処理を行わない
                        Quotations_attached_file.objects.create(
                            quotation_id=quotation,
                            file=self.request.FILES['file'],
                        )

            logger.info(
                'Quotation quotation_id:{} has been updated by Users.id:{}'.format(
                    quotation.quotation_id,
                    self.request.user.id))
            messages.success(self.request, '更新が完了しました。')
        else:
            self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        try:
            if not Clients.objects.filter(
                    pk=self.request.POST.get('client_id')).exists():
                messages.error(self.request, '顧客が存在しませんでした。')
        except ValueError:
            messages.error(self.request, '顧客フィールドには顧客IDを入力してください。')

        logger.error(
            'Quotation could not be updated by Users.id:{} \r\n{}'.format(
                self.request.user.id,
                self.request.POST))
        messages.error(self.request, '更新ができませんでした。')

        return super().form_invalid(form)


@login_required
def file_download_view(request, pk):
    file_path = str(Quotations_attached_file.objects.get(quotation_id=pk).file)
    file_path = settings.MEDIA_ROOT + '\\' + file_path.replace('/', '\\')
    file_name = file_path.split('\\')[-1]
    return FileResponse(open(file_path, "rb"),
                        as_attachment=True, filename=file_name)


@login_required
def file_delete_view(request, pk):
    Quotations_attached_file.objects.get(quotation_id=pk).delete()
    return redirect("quotation:reference", pk)


@login_required
def excel_download_view(request, pk):
    book = create_excel(request, pk)
    file_path = book['book_path']
    file_name = book['book_name']
    return FileResponse(open(file_path, "rb"),
                        as_attachment=True, filename=file_name)


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Quotations
    template_name = 'quotation_delete.html'
    success_url = reverse_lazy('quotation:list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        logger.info(
            'Quotation quotation_id:{} has been deleted by Users.id:{}'.format(
                self.kwargs['pk'],
                self.request.user.id))
        messages.success(self.request, '削除が完了しました。')
        return result
