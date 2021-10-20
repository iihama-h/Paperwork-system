from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
from datetime import datetime
from django.utils import timezone
from freezegun import freeze_time
from django.contrib.messages import get_messages
from django.core.files.base import ContentFile
import os
from shutil import rmtree
from django.conf import settings
from django.core.files import File
from paperwork_system import constant_values

from ..models import Quotations, Quotations_details, Quotations_attached_file, Clients


class Test_QuotationRegistrationView(LoggedInTestCase):

    # 事前準備
    test_directory_path = settings.MEDIA_ROOT + \
        '\\uploads\\2021\\05\\24\\'.replace('\\\\', '\\')

    if os.path.exists(test_directory_path):
        rmtree(test_directory_path)

    def setUp(self):
        super().setUp()
        # テスト用データの作成
        registration_client = Clients.objects.create(
            client_id=1,
            name='顧客名'
        )


# 正常系


    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success(self):

        file_object = ContentFile(b'file content', 'test.txt')

        params = {
            'quotation_id': 1,
            'client_id': 1,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '商品名',
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': 1,
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': 100,
            'quotations_details_set-0-purchase_unit_price': 90,

            'file': file_object
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], params['expiry'])
        self.assertEqual(queryset[0]['recipient'], params['recipient'])
        self.assertEqual(queryset[0]['title'], params['title'])
        self.assertEqual(queryset[0]['delivery_time'], params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertEqual(queryset[0]['unit'],
                         params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['file'],
            'uploads/2021/05/24/' +
            file_object.name)
        self.assertTrue(os.path.exists(self.test_directory_path))
        self.assertTrue(queryset[0]["is_active"])

        # 後処理
        os.remove(
            settings.MEDIA_ROOT +
            '\\uploads\\2021\\05\\24\\' +
            file_object.name.replace(
                '\\\\',
                '\\'))

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_max(self):

        file_object = ContentFile(b'file content', 'test.txt')

        params = {
            'quotation_id': 2,
            'client_id': 1,
            'expiry': '見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有',
            'recipient': '宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛宛名宛名宛名宛名宛名宛名宛名',
            'title': '件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名宛件名件名件名件名件名件名件名',
            'delivery_time': '納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期宛納期納期納期納期納期納期納期',
            'delivery_location': '納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場',
            'delivery_method': '納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方',
            'payment_condition': '取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条',
            'remark': '備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備',

            'quotations_details_set-TOTAL_FORMS': 3,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'quotations_details_set-0-merchandise': '商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名',
            'quotations_details_set-0-merchandise_description': '商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明',
            'quotations_details_set-0-quantity': 1,
            'quotations_details_set-0-unit': '単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単',
            'quotations_details_set-0-sales_unit_price': 2147483647,
            'quotations_details_set-0-purchase_unit_price': 2147483647,

            'quotations_details_set-1-merchandise': '商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名',
            'quotations_details_set-1-merchandise_description': '商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A',
            'quotations_details_set-1-quantity': 1,
            'quotations_details_set-1-unit': '単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A',
            'quotations_details_set-1-sales_unit_price': 2147483647,
            'quotations_details_set-1-purchase_unit_price': 2147483647,

            'quotations_details_set-2-merchandise': '商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名',
            'quotations_details_set-2-merchandise_description': '商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B',
            'quotations_details_set-2-quantity': 1,
            'quotations_details_set-2-unit': '単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B',
            'quotations_details_set-2-sales_unit_price': 2147483647,
            'quotations_details_set-2-purchase_unit_price': 2147483647,

            'file': file_object
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 3)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], params['expiry'])
        self.assertEqual(queryset[0]['recipient'], params['recipient'])
        self.assertEqual(queryset[0]['title'], params['title'])
        self.assertEqual(queryset[0]['delivery_time'], params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 644245094)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).order_by('item_id').values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertEqual(queryset[0]['unit'],
                         params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

        self.assertEqual(
            queryset[1]['item_id'], str(
                params['quotation_id']) + '_1')
        self.assertEqual(
            queryset[1]['merchandise'],
            params['quotations_details_set-1-merchandise'])
        self.assertEqual(
            queryset[1]['merchandise_description'],
            params['quotations_details_set-1-merchandise_description'])
        self.assertEqual(queryset[1]['quantity'],
                         params['quotations_details_set-1-quantity'])
        self.assertEqual(queryset[1]['unit'],
                         params['quotations_details_set-1-unit'])
        self.assertEqual(
            queryset[1]['sales_unit_price'],
            params['quotations_details_set-1-sales_unit_price'])
        self.assertEqual(
            queryset[1]['purchase_unit_price'],
            params['quotations_details_set-1-purchase_unit_price'])
        self.assertEqual(queryset[1]['order'], 1)
        self.assertTrue(queryset[1]['is_active'])

        self.assertEqual(
            queryset[2]['item_id'], str(
                params['quotation_id']) + '_2')
        self.assertEqual(
            queryset[2]['merchandise'],
            params['quotations_details_set-2-merchandise'])
        self.assertEqual(
            queryset[2]['merchandise_description'],
            params['quotations_details_set-2-merchandise_description'])
        self.assertEqual(queryset[2]['quantity'],
                         params['quotations_details_set-2-quantity'])
        self.assertEqual(queryset[2]['unit'],
                         params['quotations_details_set-2-unit'])
        self.assertEqual(
            queryset[2]['sales_unit_price'],
            params['quotations_details_set-2-sales_unit_price'])
        self.assertEqual(
            queryset[2]['purchase_unit_price'],
            params['quotations_details_set-2-purchase_unit_price'])
        self.assertEqual(queryset[2]['order'], 2)
        self.assertTrue(queryset[2]['is_active'])

        queryset = Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['file'],
            'uploads/2021/05/24/' +
            file_object.name)
        self.assertTrue(os.path.exists(self.test_directory_path))
        self.assertTrue(queryset[0]["is_active"])

        # 後処理
        os.remove(
            settings.MEDIA_ROOT +
            '\\uploads\\2021\\05\\24\\' +
            file_object.name.replace(
                '\\\\',
                '\\'))

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_max_quantity(self):

        params = {
            'quotation_id': 3,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 2147483647,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 0)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).order_by('item_id').values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertIsNone(queryset[0]['merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertIsNone(queryset[0]['unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_min(self):

        params = {
            'quotation_id': 4,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 0,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 0)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_min_integer(self):

        params = {
            'quotation_id': 5,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 1,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': -2147483648,
            'quotations_details_set-0-purchase_unit_price': -2147483648,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], -214748365)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertIsNone(queryset[0]['merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertIsNone(queryset[0]['unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_min_integer_quantity(self):

        params = {
            'quotation_id': 6,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': -2147483648,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 0)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertIsNone(queryset[0]['merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertIsNone(queryset[0]['unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_FullWidth_integer(self):

        params = {
            'quotation_id': 7,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': '１',
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': '２１４７４８３６４７',
            'quotations_details_set-0-purchase_unit_price': '２１４７４８３６４７',

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 214748364)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertIsNone(queryset[0]['merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'], 1)
        self.assertIsNone(queryset[0]['unit'])
        self.assertEqual(queryset[0]['sales_unit_price'], 2147483647)
        self.assertEqual(queryset[0]['purchase_unit_price'], 2147483647)
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2020-02-29 12:34:56")
    def Test_create_quotation_success_special(self):

        params = {
            'quotation_id': 8,
            'client_id': 1,
            'expiry': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'recipient': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'title': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'delivery_time': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'delivery_location': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'delivery_method': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'payment_condition': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'remark': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'quotations_details_set-0-merchandise_description': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'quotations_details_set-0-quantity': 0,
            'quotations_details_set-0-unit': "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2020, 2, 29, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2020, 2, 29, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], params['expiry'])
        self.assertEqual(queryset[0]['recipient'], params['recipient'])
        self.assertEqual(queryset[0]['title'], params['title'])
        self.assertEqual(queryset[0]['delivery_time'], params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 0)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertEqual(queryset[0]['unit'],
                         params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2021-05-24 12:34:56")
    # detailsの1000件登録は行わない　Excel出力の最大値25件で検証
    def Test_create_quotation_success_details_max(self):

        file_object = ContentFile(b'file content', 'test.txt')

        params = {
            'quotation_id': 9,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 25,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'quotations_details_set-0-merchandise': '0',
            'quotations_details_set-0-merchandise_description': '00',
            'quotations_details_set-0-quantity': 0,
            'quotations_details_set-0-unit': '000',
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'quotations_details_set-1-merchandise': '1',
            'quotations_details_set-1-merchandise_description': '11',
            'quotations_details_set-1-quantity': 1,
            'quotations_details_set-1-unit': '111',
            'quotations_details_set-1-sales_unit_price': 1,
            'quotations_details_set-1-purchase_unit_price': 1,

            'quotations_details_set-2-merchandise': '2',
            'quotations_details_set-2-merchandise_description': '22',
            'quotations_details_set-2-quantity': 2,
            'quotations_details_set-2-unit': '222',
            'quotations_details_set-2-sales_unit_price': 2,
            'quotations_details_set-2-purchase_unit_price': 2,

            'quotations_details_set-3-merchandise': '3',
            'quotations_details_set-3-merchandise_description': '33',
            'quotations_details_set-3-quantity': 3,
            'quotations_details_set-3-unit': '333',
            'quotations_details_set-3-sales_unit_price': 3,
            'quotations_details_set-3-purchase_unit_price': 3,

            'quotations_details_set-4-merchandise': '4',
            'quotations_details_set-4-merchandise_description': '44',
            'quotations_details_set-4-quantity': 4,
            'quotations_details_set-4-unit': '444',
            'quotations_details_set-4-sales_unit_price': 4,
            'quotations_details_set-4-purchase_unit_price': 4,

            'quotations_details_set-5-merchandise': '5',
            'quotations_details_set-5-merchandise_description': '55',
            'quotations_details_set-5-quantity': 5,
            'quotations_details_set-5-unit': '555',
            'quotations_details_set-5-sales_unit_price': 5,
            'quotations_details_set-5-purchase_unit_price': 5,

            'quotations_details_set-6-merchandise': '6',
            'quotations_details_set-6-merchandise_description': '66',
            'quotations_details_set-6-quantity': 6,
            'quotations_details_set-6-unit': '666',
            'quotations_details_set-6-sales_unit_price': 6,
            'quotations_details_set-6-purchase_unit_price': 6,

            'quotations_details_set-7-merchandise': '7',
            'quotations_details_set-7-merchandise_description': '77',
            'quotations_details_set-7-quantity': 7,
            'quotations_details_set-7-unit': '777',
            'quotations_details_set-7-sales_unit_price': 7,
            'quotations_details_set-7-purchase_unit_price': 7,

            'quotations_details_set-8-merchandise': '8',
            'quotations_details_set-8-merchandise_description': '88',
            'quotations_details_set-8-quantity': 8,
            'quotations_details_set-8-unit': '888',
            'quotations_details_set-8-sales_unit_price': 8,
            'quotations_details_set-8-purchase_unit_price': 8,

            'quotations_details_set-9-merchandise': '9',
            'quotations_details_set-9-merchandise_description': '99',
            'quotations_details_set-9-quantity': 9,
            'quotations_details_set-9-unit': '999',
            'quotations_details_set-9-sales_unit_price': 9,
            'quotations_details_set-9-purchase_unit_price': 9,

            'quotations_details_set-10-merchandise': '10',
            'quotations_details_set-10-merchandise_description': '1010',
            'quotations_details_set-10-quantity': 10,
            'quotations_details_set-10-unit': '101010',
            'quotations_details_set-10-sales_unit_price': 10,
            'quotations_details_set-10-purchase_unit_price': 10,

            'quotations_details_set-11-merchandise': '11',
            'quotations_details_set-11-merchandise_description': '1111',
            'quotations_details_set-11-quantity': 11,
            'quotations_details_set-11-unit': '111111',
            'quotations_details_set-11-sales_unit_price': 11,
            'quotations_details_set-11-purchase_unit_price': 11,

            'quotations_details_set-12-merchandise': '12',
            'quotations_details_set-12-merchandise_description': '1212',
            'quotations_details_set-12-quantity': 12,
            'quotations_details_set-12-unit': '121212',
            'quotations_details_set-12-sales_unit_price': 12,
            'quotations_details_set-12-purchase_unit_price': 12,

            'quotations_details_set-13-merchandise': '13',
            'quotations_details_set-13-merchandise_description': '1313',
            'quotations_details_set-13-quantity': 13,
            'quotations_details_set-13-unit': '131313',
            'quotations_details_set-13-sales_unit_price': 13,
            'quotations_details_set-13-purchase_unit_price': 13,

            'quotations_details_set-14-merchandise': '14',
            'quotations_details_set-14-merchandise_description': '1414',
            'quotations_details_set-14-quantity': 14,
            'quotations_details_set-14-unit': '141414',
            'quotations_details_set-14-sales_unit_price': 14,
            'quotations_details_set-14-purchase_unit_price': 14,

            'quotations_details_set-15-merchandise': '15',
            'quotations_details_set-15-merchandise_description': '1515',
            'quotations_details_set-15-quantity': 15,
            'quotations_details_set-15-unit': '151515',
            'quotations_details_set-15-sales_unit_price': 15,
            'quotations_details_set-15-purchase_unit_price': 15,

            'quotations_details_set-16-merchandise': '16',
            'quotations_details_set-16-merchandise_description': '1616',
            'quotations_details_set-16-quantity': 16,
            'quotations_details_set-16-unit': '161616',
            'quotations_details_set-16-sales_unit_price': 16,
            'quotations_details_set-16-purchase_unit_price': 16,

            'quotations_details_set-17-merchandise': '17',
            'quotations_details_set-17-merchandise_description': '1717',
            'quotations_details_set-17-quantity': 17,
            'quotations_details_set-17-unit': '171717',
            'quotations_details_set-17-sales_unit_price': 17,
            'quotations_details_set-17-purchase_unit_price': 17,

            'quotations_details_set-18-merchandise': '18',
            'quotations_details_set-18-merchandise_description': '1818',
            'quotations_details_set-18-quantity': 18,
            'quotations_details_set-18-unit': '181818',
            'quotations_details_set-18-sales_unit_price': 18,
            'quotations_details_set-18-purchase_unit_price': 18,

            'quotations_details_set-19-merchandise': '19',
            'quotations_details_set-19-merchandise_description': '1919',
            'quotations_details_set-19-quantity': 19,
            'quotations_details_set-19-unit': '191919',
            'quotations_details_set-19-sales_unit_price': 19,
            'quotations_details_set-19-purchase_unit_price': 19,

            'quotations_details_set-20-merchandise': '20',
            'quotations_details_set-20-merchandise_description': '2020',
            'quotations_details_set-20-quantity': 20,
            'quotations_details_set-20-unit': '202020',
            'quotations_details_set-20-sales_unit_price': 20,
            'quotations_details_set-20-purchase_unit_price': 20,

            'quotations_details_set-21-merchandise': '21',
            'quotations_details_set-21-merchandise_description': '2121',
            'quotations_details_set-21-quantity': 21,
            'quotations_details_set-21-unit': '212121',
            'quotations_details_set-21-sales_unit_price': 21,
            'quotations_details_set-21-purchase_unit_price': 21,

            'quotations_details_set-22-merchandise': '22',
            'quotations_details_set-22-merchandise_description': '2222',
            'quotations_details_set-22-quantity': 22,
            'quotations_details_set-22-unit': '222222',
            'quotations_details_set-22-sales_unit_price': 22,
            'quotations_details_set-22-purchase_unit_price': 22,

            'quotations_details_set-23-merchandise': '23',
            'quotations_details_set-23-merchandise_description': '2323',
            'quotations_details_set-23-quantity': 23,
            'quotations_details_set-23-unit': '232323',
            'quotations_details_set-23-sales_unit_price': 23,
            'quotations_details_set-23-purchase_unit_price': 23,

            'quotations_details_set-24-merchandise': '24',
            'quotations_details_set-24-merchandise_description': '2424',
            'quotations_details_set-24-quantity': 24,
            'quotations_details_set-24-unit': '242424',
            'quotations_details_set-24-sales_unit_price': 24,
            'quotations_details_set-24-purchase_unit_price': 24,

            'file': file_object
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 25)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(
            queryset[0]['delivery_time'],
            params['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 490)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).order_by('order').values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertEqual(queryset[0]['unit'],
                         params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

        self.assertEqual(
            queryset[1]['item_id'], str(
                params['quotation_id']) + '_1')
        self.assertEqual(
            queryset[1]['merchandise'],
            params['quotations_details_set-1-merchandise'])
        self.assertEqual(
            queryset[1]['merchandise_description'],
            params['quotations_details_set-1-merchandise_description'])
        self.assertEqual(queryset[1]['quantity'],
                         params['quotations_details_set-1-quantity'])
        self.assertEqual(queryset[1]['unit'],
                         params['quotations_details_set-1-unit'])
        self.assertEqual(
            queryset[1]['sales_unit_price'],
            params['quotations_details_set-1-sales_unit_price'])
        self.assertEqual(
            queryset[1]['purchase_unit_price'],
            params['quotations_details_set-1-purchase_unit_price'])
        self.assertEqual(queryset[1]['order'], 1)
        self.assertTrue(queryset[1]['is_active'])

        self.assertEqual(
            queryset[2]['item_id'], str(
                params['quotation_id']) + '_2')
        self.assertEqual(
            queryset[2]['merchandise'],
            params['quotations_details_set-2-merchandise'])
        self.assertEqual(
            queryset[2]['merchandise_description'],
            params['quotations_details_set-2-merchandise_description'])
        self.assertEqual(queryset[2]['quantity'],
                         params['quotations_details_set-2-quantity'])
        self.assertEqual(queryset[2]['unit'],
                         params['quotations_details_set-2-unit'])
        self.assertEqual(
            queryset[2]['sales_unit_price'],
            params['quotations_details_set-2-sales_unit_price'])
        self.assertEqual(
            queryset[2]['purchase_unit_price'],
            params['quotations_details_set-2-purchase_unit_price'])
        self.assertEqual(queryset[2]['order'], 2)
        self.assertTrue(queryset[2]['is_active'])

        self.assertEqual(
            queryset[3]['item_id'], str(
                params['quotation_id']) + '_3')
        self.assertEqual(
            queryset[3]['merchandise'],
            params['quotations_details_set-3-merchandise'])
        self.assertEqual(
            queryset[3]['merchandise_description'],
            params['quotations_details_set-3-merchandise_description'])
        self.assertEqual(queryset[3]['quantity'],
                         params['quotations_details_set-3-quantity'])
        self.assertEqual(queryset[3]['unit'],
                         params['quotations_details_set-3-unit'])
        self.assertEqual(
            queryset[3]['sales_unit_price'],
            params['quotations_details_set-3-sales_unit_price'])
        self.assertEqual(
            queryset[3]['purchase_unit_price'],
            params['quotations_details_set-3-purchase_unit_price'])
        self.assertEqual(queryset[3]['order'], 3)
        self.assertTrue(queryset[3]['is_active'])

        self.assertEqual(
            queryset[4]['item_id'], str(
                params['quotation_id']) + '_4')
        self.assertEqual(
            queryset[4]['merchandise'],
            params['quotations_details_set-4-merchandise'])
        self.assertEqual(
            queryset[4]['merchandise_description'],
            params['quotations_details_set-4-merchandise_description'])
        self.assertEqual(queryset[4]['quantity'],
                         params['quotations_details_set-4-quantity'])
        self.assertEqual(queryset[4]['unit'],
                         params['quotations_details_set-4-unit'])
        self.assertEqual(
            queryset[4]['sales_unit_price'],
            params['quotations_details_set-4-sales_unit_price'])
        self.assertEqual(
            queryset[4]['purchase_unit_price'],
            params['quotations_details_set-4-purchase_unit_price'])
        self.assertEqual(queryset[4]['order'], 4)
        self.assertTrue(queryset[4]['is_active'])

        self.assertEqual(
            queryset[5]['item_id'], str(
                params['quotation_id']) + '_5')
        self.assertEqual(
            queryset[5]['merchandise'],
            params['quotations_details_set-5-merchandise'])
        self.assertEqual(
            queryset[5]['merchandise_description'],
            params['quotations_details_set-5-merchandise_description'])
        self.assertEqual(queryset[5]['quantity'],
                         params['quotations_details_set-5-quantity'])
        self.assertEqual(queryset[5]['unit'],
                         params['quotations_details_set-5-unit'])
        self.assertEqual(
            queryset[5]['sales_unit_price'],
            params['quotations_details_set-5-sales_unit_price'])
        self.assertEqual(
            queryset[5]['purchase_unit_price'],
            params['quotations_details_set-5-purchase_unit_price'])
        self.assertEqual(queryset[5]['order'], 5)
        self.assertTrue(queryset[5]['is_active'])

        self.assertEqual(
            queryset[6]['item_id'], str(
                params['quotation_id']) + '_6')
        self.assertEqual(
            queryset[6]['merchandise'],
            params['quotations_details_set-6-merchandise'])
        self.assertEqual(
            queryset[6]['merchandise_description'],
            params['quotations_details_set-6-merchandise_description'])
        self.assertEqual(queryset[6]['quantity'],
                         params['quotations_details_set-6-quantity'])
        self.assertEqual(queryset[6]['unit'],
                         params['quotations_details_set-6-unit'])
        self.assertEqual(
            queryset[6]['sales_unit_price'],
            params['quotations_details_set-6-sales_unit_price'])
        self.assertEqual(
            queryset[6]['purchase_unit_price'],
            params['quotations_details_set-6-purchase_unit_price'])
        self.assertEqual(queryset[6]['order'], 6)
        self.assertTrue(queryset[6]['is_active'])

        self.assertEqual(
            queryset[7]['item_id'], str(
                params['quotation_id']) + '_7')
        self.assertEqual(
            queryset[7]['merchandise'],
            params['quotations_details_set-7-merchandise'])
        self.assertEqual(
            queryset[7]['merchandise_description'],
            params['quotations_details_set-7-merchandise_description'])
        self.assertEqual(queryset[7]['quantity'],
                         params['quotations_details_set-7-quantity'])
        self.assertEqual(queryset[7]['unit'],
                         params['quotations_details_set-7-unit'])
        self.assertEqual(
            queryset[7]['sales_unit_price'],
            params['quotations_details_set-7-sales_unit_price'])
        self.assertEqual(
            queryset[7]['purchase_unit_price'],
            params['quotations_details_set-7-purchase_unit_price'])
        self.assertEqual(queryset[7]['order'], 7)
        self.assertTrue(queryset[7]['is_active'])

        self.assertEqual(
            queryset[8]['item_id'], str(
                params['quotation_id']) + '_8')
        self.assertEqual(
            queryset[8]['merchandise'],
            params['quotations_details_set-8-merchandise'])
        self.assertEqual(
            queryset[8]['merchandise_description'],
            params['quotations_details_set-8-merchandise_description'])
        self.assertEqual(queryset[8]['quantity'],
                         params['quotations_details_set-8-quantity'])
        self.assertEqual(queryset[8]['unit'],
                         params['quotations_details_set-8-unit'])
        self.assertEqual(
            queryset[8]['sales_unit_price'],
            params['quotations_details_set-8-sales_unit_price'])
        self.assertEqual(
            queryset[8]['purchase_unit_price'],
            params['quotations_details_set-8-purchase_unit_price'])
        self.assertEqual(queryset[8]['order'], 8)
        self.assertTrue(queryset[8]['is_active'])

        self.assertEqual(
            queryset[9]['item_id'], str(
                params['quotation_id']) + '_9')
        self.assertEqual(
            queryset[9]['merchandise'],
            params['quotations_details_set-9-merchandise'])
        self.assertEqual(
            queryset[9]['merchandise_description'],
            params['quotations_details_set-9-merchandise_description'])
        self.assertEqual(queryset[9]['quantity'],
                         params['quotations_details_set-9-quantity'])
        self.assertEqual(queryset[9]['unit'],
                         params['quotations_details_set-9-unit'])
        self.assertEqual(
            queryset[9]['sales_unit_price'],
            params['quotations_details_set-9-sales_unit_price'])
        self.assertEqual(
            queryset[9]['purchase_unit_price'],
            params['quotations_details_set-9-purchase_unit_price'])
        self.assertEqual(queryset[9]['order'], 9)
        self.assertTrue(queryset[9]['is_active'])

        self.assertEqual(
            queryset[10]['item_id'], str(
                params['quotation_id']) + '_10')
        self.assertEqual(
            queryset[10]['merchandise'],
            params['quotations_details_set-10-merchandise'])
        self.assertEqual(
            queryset[10]['merchandise_description'],
            params['quotations_details_set-10-merchandise_description'])
        self.assertEqual(queryset[10]['quantity'],
                         params['quotations_details_set-10-quantity'])
        self.assertEqual(queryset[10]['unit'],
                         params['quotations_details_set-10-unit'])
        self.assertEqual(
            queryset[10]['sales_unit_price'],
            params['quotations_details_set-10-sales_unit_price'])
        self.assertEqual(
            queryset[10]['purchase_unit_price'],
            params['quotations_details_set-10-purchase_unit_price'])
        self.assertEqual(queryset[10]['order'], 10)
        self.assertTrue(queryset[10]['is_active'])

        self.assertEqual(
            queryset[11]['item_id'], str(
                params['quotation_id']) + '_11')
        self.assertEqual(
            queryset[11]['merchandise'],
            params['quotations_details_set-11-merchandise'])
        self.assertEqual(
            queryset[11]['merchandise_description'],
            params['quotations_details_set-11-merchandise_description'])
        self.assertEqual(queryset[11]['quantity'],
                         params['quotations_details_set-11-quantity'])
        self.assertEqual(queryset[11]['unit'],
                         params['quotations_details_set-11-unit'])
        self.assertEqual(
            queryset[11]['sales_unit_price'],
            params['quotations_details_set-11-sales_unit_price'])
        self.assertEqual(
            queryset[11]['purchase_unit_price'],
            params['quotations_details_set-11-purchase_unit_price'])
        self.assertEqual(queryset[11]['order'], 11)
        self.assertTrue(queryset[11]['is_active'])

        self.assertEqual(
            queryset[12]['item_id'], str(
                params['quotation_id']) + '_12')
        self.assertEqual(
            queryset[12]['merchandise'],
            params['quotations_details_set-12-merchandise'])
        self.assertEqual(
            queryset[12]['merchandise_description'],
            params['quotations_details_set-12-merchandise_description'])
        self.assertEqual(queryset[12]['quantity'],
                         params['quotations_details_set-12-quantity'])
        self.assertEqual(queryset[12]['unit'],
                         params['quotations_details_set-12-unit'])
        self.assertEqual(
            queryset[12]['sales_unit_price'],
            params['quotations_details_set-12-sales_unit_price'])
        self.assertEqual(
            queryset[12]['purchase_unit_price'],
            params['quotations_details_set-12-purchase_unit_price'])
        self.assertEqual(queryset[12]['order'], 12)
        self.assertTrue(queryset[12]['is_active'])

        self.assertEqual(
            queryset[13]['item_id'], str(
                params['quotation_id']) + '_13')
        self.assertEqual(
            queryset[13]['merchandise'],
            params['quotations_details_set-13-merchandise'])
        self.assertEqual(
            queryset[13]['merchandise_description'],
            params['quotations_details_set-13-merchandise_description'])
        self.assertEqual(queryset[13]['quantity'],
                         params['quotations_details_set-13-quantity'])
        self.assertEqual(queryset[13]['unit'],
                         params['quotations_details_set-13-unit'])
        self.assertEqual(
            queryset[13]['sales_unit_price'],
            params['quotations_details_set-13-sales_unit_price'])
        self.assertEqual(
            queryset[13]['purchase_unit_price'],
            params['quotations_details_set-13-purchase_unit_price'])
        self.assertEqual(queryset[13]['order'], 13)
        self.assertTrue(queryset[13]['is_active'])

        self.assertEqual(
            queryset[14]['item_id'], str(
                params['quotation_id']) + '_14')
        self.assertEqual(
            queryset[14]['merchandise'],
            params['quotations_details_set-14-merchandise'])
        self.assertEqual(
            queryset[14]['merchandise_description'],
            params['quotations_details_set-14-merchandise_description'])
        self.assertEqual(queryset[14]['quantity'],
                         params['quotations_details_set-14-quantity'])
        self.assertEqual(queryset[14]['unit'],
                         params['quotations_details_set-14-unit'])
        self.assertEqual(
            queryset[14]['sales_unit_price'],
            params['quotations_details_set-14-sales_unit_price'])
        self.assertEqual(
            queryset[14]['purchase_unit_price'],
            params['quotations_details_set-14-purchase_unit_price'])
        self.assertEqual(queryset[14]['order'], 14)
        self.assertTrue(queryset[14]['is_active'])

        self.assertEqual(
            queryset[15]['item_id'], str(
                params['quotation_id']) + '_15')
        self.assertEqual(
            queryset[15]['merchandise'],
            params['quotations_details_set-15-merchandise'])
        self.assertEqual(
            queryset[15]['merchandise_description'],
            params['quotations_details_set-15-merchandise_description'])
        self.assertEqual(queryset[15]['quantity'],
                         params['quotations_details_set-15-quantity'])
        self.assertEqual(queryset[15]['unit'],
                         params['quotations_details_set-15-unit'])
        self.assertEqual(
            queryset[15]['sales_unit_price'],
            params['quotations_details_set-15-sales_unit_price'])
        self.assertEqual(
            queryset[15]['purchase_unit_price'],
            params['quotations_details_set-15-purchase_unit_price'])
        self.assertEqual(queryset[15]['order'], 15)
        self.assertTrue(queryset[15]['is_active'])

        self.assertEqual(
            queryset[16]['item_id'], str(
                params['quotation_id']) + '_16')
        self.assertEqual(
            queryset[16]['merchandise'],
            params['quotations_details_set-16-merchandise'])
        self.assertEqual(
            queryset[16]['merchandise_description'],
            params['quotations_details_set-16-merchandise_description'])
        self.assertEqual(queryset[16]['quantity'],
                         params['quotations_details_set-16-quantity'])
        self.assertEqual(queryset[16]['unit'],
                         params['quotations_details_set-16-unit'])
        self.assertEqual(
            queryset[16]['sales_unit_price'],
            params['quotations_details_set-16-sales_unit_price'])
        self.assertEqual(
            queryset[16]['purchase_unit_price'],
            params['quotations_details_set-16-purchase_unit_price'])
        self.assertEqual(queryset[16]['order'], 16)
        self.assertTrue(queryset[16]['is_active'])

        self.assertEqual(
            queryset[17]['item_id'], str(
                params['quotation_id']) + '_17')
        self.assertEqual(
            queryset[17]['merchandise'],
            params['quotations_details_set-17-merchandise'])
        self.assertEqual(
            queryset[17]['merchandise_description'],
            params['quotations_details_set-17-merchandise_description'])
        self.assertEqual(queryset[17]['quantity'],
                         params['quotations_details_set-17-quantity'])
        self.assertEqual(queryset[17]['unit'],
                         params['quotations_details_set-17-unit'])
        self.assertEqual(
            queryset[17]['sales_unit_price'],
            params['quotations_details_set-17-sales_unit_price'])
        self.assertEqual(
            queryset[17]['purchase_unit_price'],
            params['quotations_details_set-17-purchase_unit_price'])
        self.assertEqual(queryset[17]['order'], 17)
        self.assertTrue(queryset[17]['is_active'])

        self.assertEqual(
            queryset[18]['item_id'], str(
                params['quotation_id']) + '_18')
        self.assertEqual(
            queryset[18]['merchandise'],
            params['quotations_details_set-18-merchandise'])
        self.assertEqual(
            queryset[18]['merchandise_description'],
            params['quotations_details_set-18-merchandise_description'])
        self.assertEqual(queryset[18]['quantity'],
                         params['quotations_details_set-18-quantity'])
        self.assertEqual(queryset[18]['unit'],
                         params['quotations_details_set-18-unit'])
        self.assertEqual(
            queryset[18]['sales_unit_price'],
            params['quotations_details_set-18-sales_unit_price'])
        self.assertEqual(
            queryset[18]['purchase_unit_price'],
            params['quotations_details_set-18-purchase_unit_price'])
        self.assertEqual(queryset[18]['order'], 18)
        self.assertTrue(queryset[18]['is_active'])

        self.assertEqual(
            queryset[19]['item_id'], str(
                params['quotation_id']) + '_19')
        self.assertEqual(
            queryset[19]['merchandise'],
            params['quotations_details_set-19-merchandise'])
        self.assertEqual(
            queryset[19]['merchandise_description'],
            params['quotations_details_set-19-merchandise_description'])
        self.assertEqual(queryset[19]['quantity'],
                         params['quotations_details_set-19-quantity'])
        self.assertEqual(queryset[19]['unit'],
                         params['quotations_details_set-19-unit'])
        self.assertEqual(
            queryset[19]['sales_unit_price'],
            params['quotations_details_set-19-sales_unit_price'])
        self.assertEqual(
            queryset[19]['purchase_unit_price'],
            params['quotations_details_set-19-purchase_unit_price'])
        self.assertEqual(queryset[19]['order'], 19)
        self.assertTrue(queryset[19]['is_active'])

        self.assertEqual(
            queryset[20]['item_id'], str(
                params['quotation_id']) + '_20')
        self.assertEqual(
            queryset[20]['merchandise'],
            params['quotations_details_set-20-merchandise'])
        self.assertEqual(
            queryset[20]['merchandise_description'],
            params['quotations_details_set-20-merchandise_description'])
        self.assertEqual(queryset[20]['quantity'],
                         params['quotations_details_set-20-quantity'])
        self.assertEqual(queryset[20]['unit'],
                         params['quotations_details_set-20-unit'])
        self.assertEqual(
            queryset[20]['sales_unit_price'],
            params['quotations_details_set-20-sales_unit_price'])
        self.assertEqual(
            queryset[20]['purchase_unit_price'],
            params['quotations_details_set-20-purchase_unit_price'])
        self.assertEqual(queryset[20]['order'], 20)
        self.assertTrue(queryset[20]['is_active'])

        self.assertEqual(
            queryset[21]['item_id'], str(
                params['quotation_id']) + '_21')
        self.assertEqual(
            queryset[21]['merchandise'],
            params['quotations_details_set-21-merchandise'])
        self.assertEqual(
            queryset[21]['merchandise_description'],
            params['quotations_details_set-21-merchandise_description'])
        self.assertEqual(queryset[21]['quantity'],
                         params['quotations_details_set-21-quantity'])
        self.assertEqual(queryset[21]['unit'],
                         params['quotations_details_set-21-unit'])
        self.assertEqual(
            queryset[21]['sales_unit_price'],
            params['quotations_details_set-21-sales_unit_price'])
        self.assertEqual(
            queryset[21]['purchase_unit_price'],
            params['quotations_details_set-21-purchase_unit_price'])
        self.assertEqual(queryset[21]['order'], 21)
        self.assertTrue(queryset[21]['is_active'])

        self.assertEqual(
            queryset[22]['item_id'], str(
                params['quotation_id']) + '_22')
        self.assertEqual(
            queryset[22]['merchandise'],
            params['quotations_details_set-22-merchandise'])
        self.assertEqual(
            queryset[22]['merchandise_description'],
            params['quotations_details_set-22-merchandise_description'])
        self.assertEqual(queryset[22]['quantity'],
                         params['quotations_details_set-22-quantity'])
        self.assertEqual(queryset[22]['unit'],
                         params['quotations_details_set-22-unit'])
        self.assertEqual(
            queryset[22]['sales_unit_price'],
            params['quotations_details_set-22-sales_unit_price'])
        self.assertEqual(
            queryset[22]['purchase_unit_price'],
            params['quotations_details_set-22-purchase_unit_price'])
        self.assertEqual(queryset[22]['order'], 22)
        self.assertTrue(queryset[22]['is_active'])

        self.assertEqual(
            queryset[23]['item_id'], str(
                params['quotation_id']) + '_23')
        self.assertEqual(
            queryset[23]['merchandise'],
            params['quotations_details_set-23-merchandise'])
        self.assertEqual(
            queryset[23]['merchandise_description'],
            params['quotations_details_set-23-merchandise_description'])
        self.assertEqual(queryset[23]['quantity'],
                         params['quotations_details_set-23-quantity'])
        self.assertEqual(queryset[23]['unit'],
                         params['quotations_details_set-23-unit'])
        self.assertEqual(
            queryset[23]['sales_unit_price'],
            params['quotations_details_set-23-sales_unit_price'])
        self.assertEqual(
            queryset[23]['purchase_unit_price'],
            params['quotations_details_set-23-purchase_unit_price'])
        self.assertEqual(queryset[23]['order'], 23)
        self.assertTrue(queryset[23]['is_active'])

        self.assertEqual(
            queryset[24]['item_id'], str(
                params['quotation_id']) + '_24')
        self.assertEqual(
            queryset[24]['merchandise'],
            params['quotations_details_set-24-merchandise'])
        self.assertEqual(
            queryset[24]['merchandise_description'],
            params['quotations_details_set-24-merchandise_description'])
        self.assertEqual(queryset[24]['quantity'],
                         params['quotations_details_set-24-quantity'])
        self.assertEqual(queryset[24]['unit'],
                         params['quotations_details_set-24-unit'])
        self.assertEqual(
            queryset[24]['sales_unit_price'],
            params['quotations_details_set-24-sales_unit_price'])
        self.assertEqual(
            queryset[24]['purchase_unit_price'],
            params['quotations_details_set-24-purchase_unit_price'])
        self.assertEqual(queryset[24]['order'], 24)
        self.assertTrue(queryset[24]['is_active'])

        queryset = Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['file'],
            'uploads/2021/05/24/' +
            file_object.name)
        self.assertTrue(os.path.exists(self.test_directory_path))
        self.assertTrue(queryset[0]["is_active"])

        # 後処理
        os.remove(
            settings.MEDIA_ROOT +
            '\\uploads\\2021\\05\\24\\' +
            file_object.name.replace(
                '\\\\',
                '\\'))

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_max_consumption_tax(self):

        params = {
            'quotation_id': 10,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 10,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': 2147483647,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 2147483647)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).order_by('item_id').values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertIsNone(queryset[0]['merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertIsNone(queryset[0]['unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_success_min_consumption_tax(self):

        params = {
            'quotation_id': 11,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 10,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': -2147483647,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0001)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 1)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=params['quotation_id']).values()
        self.assertEqual(queryset[0]['client_id_id'], params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]['expiry'])
        self.assertIsNone(queryset[0]['recipient'])
        self.assertIsNone(queryset[0]['title'])
        self.assertIsNone(queryset[0]['delivery_time'])
        self.assertIsNone(queryset[0]['delivery_location'])
        self.assertIsNone(queryset[0]['delivery_method'])
        self.assertIsNone(queryset[0]['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], -2147483647)
        self.assertEqual(queryset[0]['remark'], params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).order_by('item_id').values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                params['quotation_id']) + '_0')
        self.assertIsNone(queryset[0]['merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'],
                         params['quotations_details_set-0-quantity'])
        self.assertIsNone(queryset[0]['unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])


# 異常系


    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_no_Requiredfield(self):

        params = {
            'quotation_id': 12,
            'client_id': '',
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': '',
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': '',
            'quotations_details_set-0-purchase_unit_price': '',

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'client_id', 'このフィールドは必須です。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0004)
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_max(self):

        file_object = ContentFile(b'file content', 'test.txt')

        params = {
            'quotation_id': 12,
            'client_id': 1,
            'expiry': '見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効期限見積有効',
            'recipient': '宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛名宛宛名宛名宛名宛名宛名宛名宛名宛',
            'title': '件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名件名宛件名件名件名件名件名件名件名件',
            'delivery_time': '納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期納期宛納期納期納期納期納期納期納期納',
            'delivery_location': '納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所納入場所',
            'delivery_method': '納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法納入方法',
            'payment_condition': '取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件取引条件',
            'remark': '備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考備考',

            'quotations_details_set-TOTAL_FORMS': 3,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'quotations_details_set-0-merchandise': '商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商品名商',
            'quotations_details_set-0-merchandise_description': '商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細商品明細',
            'quotations_details_set-0-quantity': 2147483648,
            'quotations_details_set-0-unit': '単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位単位',
            'quotations_details_set-0-sales_unit_price': 2147483648,
            'quotations_details_set-0-purchase_unit_price': 2147483648,

            'quotations_details_set-1-merchandise': '商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A商品名A',
            'quotations_details_set-1-merchandise_description': '商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商品明細A商',
            'quotations_details_set-1-quantity': 2147483648,
            'quotations_details_set-1-unit': '単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単位A単',
            'quotations_details_set-1-sales_unit_price': 2147483648,
            'quotations_details_set-1-purchase_unit_price': 2147483648,

            'quotations_details_set-2-merchandise': '商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B商品名B',
            'quotations_details_set-2-merchandise_description': '商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商品明細B商',
            'quotations_details_set-2-quantity': 2147483648,
            'quotations_details_set-2-unit': '単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単位B単',
            'quotations_details_set-2-sales_unit_price': 2147483648,
            'quotations_details_set-2-purchase_unit_price': 2147483648,
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(
            response,
            'form',
            'expiry',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'recipient',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'title',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'delivery_time',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'delivery_location',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'delivery_method',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'payment_condition',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'merchandise',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'quantity',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'unit',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'sales_unit_price',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'purchase_unit_price',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            1,
            'merchandise',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            1,
            'quantity',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            1,
            'unit',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            1,
            'sales_unit_price',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            1,
            'purchase_unit_price',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            2,
            'merchandise',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            2,
            'quantity',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            2,
            'unit',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            2,
            'sales_unit_price',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            2,
            'purchase_unit_price',
            'この値は 2147483647 以下でなければなりません。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_min_integer(self):

        params = {
            'quotation_id': 12,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '商品名',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': -2147483649,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': -2147483649,
            'quotations_details_set-0-purchase_unit_price': -2147483649,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'quantity',
            'この値は -2147483648 以上でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'sales_unit_price',
            'この値は -2147483648 以上でなければなりません。')
        self.assertFormsetError(
            response,
            'Quotations_details_form',
            0,
            'purchase_unit_price',
            'この値は -2147483648 以上でなければなりません。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_not_client_id(self):

        params = {
            'quotation_id': 12,
            'client_id': '顧客名',
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '商品名',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': '',
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': '',
            'quotations_details_set-0-purchase_unit_price': '',

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(
            response,
            'form',
            'client_id',
            '正しく選択してください。選択したものは候補にありません。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0004)
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_client_id_not_active(self):

        params = {
            'quotation_id': 12,
            'client_id': 2,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '商品名',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': '',
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': '',
            'quotations_details_set-0-purchase_unit_price': '',

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0003)
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_max_consumption_tax(self):

        params = {
            'quotation_id': 12,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '商品名',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 20,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': 1073741824,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), constant_values.ERR_MESSAGE_0005)
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

    @freeze_time("2021-05-24 12:34:56")
    def Test_create_quotation_failure_min_consumption_tax(self):

        params = {
            'quotation_id': 12,
            'client_id': 1,
            'expiry': '',
            'recipient': '',
            'title': '',
            'delivery_time': '',
            'delivery_location': '',
            'delivery_method': '',
            'payment_condition': '',
            'remark': '',

            'quotations_details_set-TOTAL_FORMS': 1,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,
            'quotations_details_set-0-merchandise': '商品名',
            'quotations_details_set-0-merchandise_description': '',
            'quotations_details_set-0-quantity': 20,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': -1073741824,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        response = self.client.post(
            reverse_lazy('quotation:registration'), params)

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), constant_values.ERR_MESSAGE_0005)
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0001)

        # DBに登録されていないことを検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)
        self.assertEqual(Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).count(), 0)

# Quotationsモデルの主キー（quotation_id）がAutoFieldのため、採番される値（登録される順番）を明確にする必要あり　そのため、テスト実行順を定義する
# Djangoのテストは「test~」メソッドが実行されるたびにDBが初期化される。Djangoにテストメソッドとして認識されるのは、「test_list_quotation_success_ordering」のみであるため、各々「Test_list_quotation_~」メソッドが完了したあとも、DBの初期化処理は行われない

    def test_create_quotation_ordering(self):
        self.Test_create_quotation_success()
        self.Test_create_quotation_success_max()
        self.Test_create_quotation_success_max_quantity()
        self.Test_create_quotation_success_min()
        self.Test_create_quotation_success_min_integer()
        self.Test_create_quotation_success_min_integer_quantity()
        self.Test_create_quotation_success_FullWidth_integer()
        self.Test_create_quotation_success_special()
        self.Test_create_quotation_success_details_max()
        self.Test_create_quotation_success_max_consumption_tax()
        self.Test_create_quotation_success_min_consumption_tax()
        self.Test_create_quotation_failure_no_Requiredfield()
        self.Test_create_quotation_failure_max()
        self.Test_create_quotation_failure_min_integer()
        self.Test_create_quotation_failure_not_client_id()
        self.Test_create_quotation_failure_client_id_not_active()
        self.Test_create_quotation_failure_max_consumption_tax()
        self.Test_create_quotation_failure_min_consumption_tax()
