from django import forms
from .models import Clients


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = (
            'name',
            'name_kana',
            'department',
            'industry',
            'capital',
            'postcode',
            'address',
            'phone_number',
            'email',
            'fax_number',
            'revenue',
            'profit',
            'number_of_employees',
            'remark')
        labels = {
            'name': '顧客名',
            'name_kana': '顧客名フリガナ',
            'department': '部署',
            'industry': '業種',
            'capital': '資本金(千円)',
            'postcode': '郵便番号',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メールアドレス',
            'fax_number': 'FAX番号',
            'revenue': '売上高(百万円)',
            'profit': '利益(千円)',
            'number_of_employees': '従業員数',
            'remark': '備考'
        }


class SearchForm(forms.Form):
    name = forms.CharField(initial='', label='顧客名', required=False)
    name_kana = forms.CharField(initial='', label='顧客名フリガナ', required=False)
