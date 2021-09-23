from django import forms
from .models import Quotations, Quotations_details, Quotations_attached_file
from bootstrap_datepicker_plus import DatePickerInput


class QuotationsForm(forms.ModelForm):
    class Meta:
        model = Quotations
        fields = (
            'client_id',
            'expiry',
            'recipient',
            'title',
            'delivery_time',
            'delivery_location',
            'delivery_method',
            'payment_condition',
            'remark')
        widgets = {
            'client_id': forms.TextInput(
                attrs={
                    'required': True,
                    'id': 'id_client_id'})}
        labels = {
            'client_id': '顧客',
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',
        }


Quotations_details_formSet = forms.inlineformset_factory(
    parent_model=Quotations,
    model=Quotations_details,
    fields=(
        'merchandise',
        'merchandise_description',
        'quantity',
        'unit',
        'sales_unit_price',
        'purchase_unit_price',
        'is_active'),
    can_delete=False,
    extra=1,
    widgets={
        'is_active': forms.HiddenInput(), 'quantity': forms.NumberInput(
            attrs={
                'required': True}), 'sales_unit_price': forms.NumberInput(
            attrs={
                'required': True}), 'purchase_unit_price': forms.NumberInput(
            attrs={
                'required': True})},
    labels={
        'merchandise': '商品名',
        'merchandise_description': '商品明細',
        'quantity': '数量',
        'unit': '単位',
        'sales_unit_price': '売上単価',
        'purchase_unit_price': '仕入単価',
    }
)


class Quotations_attached_file_Form(forms.ModelForm):
    class Meta:
        parent_model = Quotations,
        model = Quotations_attached_file
        fields = ('file',)
        labels = {
            'file': '添付ファイル',
        }


class SearchForm(forms.Form):
    name = forms.CharField(initial='', label='顧客名', required=False)
    username = forms.CharField(initial='', label='登録者', required=False)
    updated_datetime = forms.DateField(
        widget=DatePickerInput(
            format='%Y-%m-%d',
            options={
                'locale': 'ja',
                'dayViewHeaderFormat': 'YYYY年 MMMM',
                'ignoreReadonly': True,
                'allowInputToggle': True}),
        label='更新日',
        required=False)
    title = forms.CharField(initial='', label='件名', required=False)
