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
from paperwork_system import constant_values

from ..models import Quotations, Quotations_details, Quotations_attached_file, Clients


class Test_QuotationReferenceView(LoggedInTestCase):

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

    def Test_update_quotation_success(self):

        registration_params = {
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行
        reference_client = Clients.objects.create(
            client_id=2,
            name='新しい顧客名'
        )

        file_object = ContentFile(b'file content', 'test.txt')

        reference_params = {
            'client_id': reference_client.client_id,
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], reference_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            reference_params['recipient'])
        self.assertEqual(queryset[0]['title'], reference_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            reference_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            reference_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            reference_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            reference_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

        queryset = Quotations_attached_file.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
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

    def Test_update_quotation_success_max(self):

        registration_params = {
            'quotation_id': 2,
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

            'file': ''
        }
        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        file_object = ContentFile(b'file content', 'test.txt')

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], reference_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            reference_params['recipient'])
        self.assertEqual(queryset[0]['title'], reference_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            reference_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            reference_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            reference_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            reference_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 644245094)
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

        self.assertEqual(queryset[1]['item_id'], str(
            registration_params['quotation_id']) + '_1')
        self.assertEqual(
            queryset[1]['merchandise'],
            reference_params['quotations_details_set-1-merchandise'])
        self.assertEqual(
            queryset[1]['merchandise_description'],
            reference_params['quotations_details_set-1-merchandise_description'])
        self.assertEqual(
            queryset[1]['quantity'],
            reference_params['quotations_details_set-1-quantity'])
        self.assertEqual(
            queryset[1]['unit'],
            reference_params['quotations_details_set-1-unit'])
        self.assertEqual(
            queryset[1]['sales_unit_price'],
            reference_params['quotations_details_set-1-sales_unit_price'])
        self.assertEqual(
            queryset[1]['purchase_unit_price'],
            reference_params['quotations_details_set-1-purchase_unit_price'])
        self.assertEqual(queryset[1]['order'], 1)
        self.assertTrue(queryset[1]['is_active'])

        self.assertEqual(queryset[2]['item_id'], str(
            registration_params['quotation_id']) + '_2')
        self.assertEqual(
            queryset[2]['merchandise'],
            reference_params['quotations_details_set-2-merchandise'])
        self.assertEqual(
            queryset[2]['merchandise_description'],
            reference_params['quotations_details_set-2-merchandise_description'])
        self.assertEqual(
            queryset[2]['quantity'],
            reference_params['quotations_details_set-2-quantity'])
        self.assertEqual(
            queryset[2]['unit'],
            reference_params['quotations_details_set-2-unit'])
        self.assertEqual(
            queryset[2]['sales_unit_price'],
            reference_params['quotations_details_set-2-sales_unit_price'])
        self.assertEqual(
            queryset[2]['purchase_unit_price'],
            reference_params['quotations_details_set-2-purchase_unit_price'])
        self.assertEqual(queryset[2]['order'], 2)
        self.assertTrue(queryset[2]['is_active'])

        self.assertEqual(len(queryset), 3)

        queryset = Quotations_attached_file.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
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

    def Test_update_quotation_success_max_quantity(self):
        registration_params = {
            'quotation_id': 3,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': 2147483647,
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(len(queryset), 1)

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_success_min(self):

        registration_params = {
            'quotation_id': 4,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(len(queryset), 0)

    def Test_update_quotation_success_min_integer(self):

        registration_params = {
            'quotation_id': 5,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': 1,
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': -2147483647,
            'quotations_details_set-0-purchase_unit_price': -2147483647,

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_success_min_integer_quantity(self):

        registration_params = {
            'quotation_id': 6,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': -2147483647,
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': 0,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_success_FullWidth_integer(self):

        registration_params = {
            'quotation_id': 7,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': '１',
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': '２１４７４８３６４７',
            'quotations_details_set-0-purchase_unit_price': '２１４７４８３６４７',

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(queryset[0]['quantity'], 1)
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(queryset[0]['sales_unit_price'], 2147483647)
        self.assertEqual(queryset[0]['purchase_unit_price'], 2147483647)
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_success_special(self):

        registration_params = {
            'quotation_id': 8,
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

            'file': ''
        }

        with freeze_time("2020-02-28 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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

        with freeze_time("2020-02-29 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2020, 2, 28, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2020, 2, 29, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], reference_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            reference_params['recipient'])
        self.assertEqual(queryset[0]['title'], reference_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            reference_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            reference_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            reference_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            reference_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 0)
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    # detailsの1000件登録は行わない　Excel出力の最大値25件で検証
    def Test_update_quotation_success_details_max(self):

        registration_params = {
            'quotation_id': 9,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行
        file_object = ContentFile(b'file content', 'test.txt')

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['consumption_tax'], 490)
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_0').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_1').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_1')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-1-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-1-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-1-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-1-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-1-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-1-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 1)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_2').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_2')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-2-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-2-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-2-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-2-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-2-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-2-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 2)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_3').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_3')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-3-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-3-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-3-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-3-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-3-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-3-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 3)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_4').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_4')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-4-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-4-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-4-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-4-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-4-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-4-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 4)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_5').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_5')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-5-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-5-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-5-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-5-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-5-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-5-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 5)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_6').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_6')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-6-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-6-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-6-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-6-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-6-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-6-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 6)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_7').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_7')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-7-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-7-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-7-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-7-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-7-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-7-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 7)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_8').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_8')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-8-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-8-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-8-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-8-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-8-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-8-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 8)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_9').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_9')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-9-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-9-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-9-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-9-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-9-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-9-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 9)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_10').values()
        self.assertEqual(
            queryset[0]['item_id'], str(
                registration_params['quotation_id']) + '_10')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-10-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-10-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-10-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-10-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-10-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-10-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 10)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_11').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_11')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-11-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-11-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-11-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-11-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-11-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-11-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 11)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_12').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_12')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-12-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-12-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-12-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-12-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-12-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-12-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 12)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_13').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_13')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-13-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-13-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-13-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-13-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-13-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-13-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 13)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_14').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_14')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-14-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-14-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-14-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-14-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-14-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-14-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 14)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_15').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_15')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-15-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-15-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-15-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-15-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-15-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-15-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 15)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_16').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_16')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-16-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-16-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-16-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-16-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-16-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-16-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 16)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_17').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_17')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-17-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-17-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-17-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-17-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-17-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-17-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 17)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_18').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_18')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-18-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-18-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-18-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-18-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-18-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-18-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 18)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_19').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_19')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-19-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-19-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-19-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-19-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-19-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-19-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 19)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_20').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_20')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-20-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-20-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-20-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-20-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-20-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-20-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 20)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_21').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_21')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-21-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-21-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-21-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-21-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-21-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-21-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 21)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_22').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_22')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-22-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-22-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-22-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-22-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-22-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-22-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 22)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_23').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_23')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-23-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-23-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-23-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-23-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-23-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-23-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 23)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(item_id=str(
            registration_params['quotation_id']) + '_24').values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_24')
        self.assertEqual(
            queryset[0]['merchandise'],
            reference_params['quotations_details_set-24-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            reference_params['quotations_details_set-24-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            reference_params['quotations_details_set-24-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            reference_params['quotations_details_set-24-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            reference_params['quotations_details_set-24-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            reference_params['quotations_details_set-24-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 24)
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).order_by('item_id').values()
        self.assertEqual(len(queryset), 25)

        queryset = Quotations_attached_file.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
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

    def Test_update_quotation_success_max_consumption_tax(self):

        registration_params = {
            'quotation_id': 10,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_success_min_consumption_tax(self):

        registration_params = {
            'quotation_id': 11,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'quotation:reference', kwargs={
                    'pk': registration_params['quotation_id']}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            reference_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
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
        self.assertEqual(queryset[0]['remark'], reference_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(len(queryset), 1)


# 異常系

    def Test_update_quotation_failure_no_Requiredfield(self):

        registration_params = {
            'quotation_id': 12,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'client_id', 'このフィールドは必須です。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0004)
        self.assertEqual(str(messages[2]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            registration_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], registration_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            registration_params['recipient'])
        self.assertEqual(queryset[0]['title'], registration_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            registration_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            registration_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            registration_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            registration_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], registration_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            registration_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            registration_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            registration_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            registration_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            registration_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            registration_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_failure_max(self):

        registration_params = {
            'quotation_id': 13,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # 必須フォームフィールドが未入力によりエラーになることを検証
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
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            registration_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], registration_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            registration_params['recipient'])
        self.assertEqual(queryset[0]['title'], registration_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            registration_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            registration_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            registration_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            registration_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], registration_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            registration_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            registration_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            registration_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            registration_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            registration_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            registration_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_failure_min_integer(self):

        registration_params = {
            'quotation_id': 14,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-quantity': -2147483649,
            'quotations_details_set-0-unit': '',
            'quotations_details_set-0-sales_unit_price': -2147483649,
            'quotations_details_set-0-purchase_unit_price': -2147483649,

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # 必須フォームフィールドが未入力によりエラーになることを検証
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
        self.assertEqual(str(messages[1]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            registration_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], registration_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            registration_params['recipient'])
        self.assertEqual(queryset[0]['title'], registration_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            registration_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            registration_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            registration_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            registration_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], registration_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            registration_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            registration_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            registration_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            registration_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            registration_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            registration_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_failure_max_consumption_tax(self):

        registration_params = {
            'quotation_id': 15,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': 20,
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': 1073741824,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), constant_values.ERR_MESSAGE_0006)
        self.assertEqual(str(messages[2]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            registration_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], registration_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            registration_params['recipient'])
        self.assertEqual(queryset[0]['title'], registration_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            registration_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            registration_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            registration_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            registration_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], registration_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            registration_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            registration_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            registration_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            registration_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            registration_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            registration_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

    def Test_update_quotation_failure_min_consumption_tax(self):

        registration_params = {
            'quotation_id': 16,
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

            'file': ''
        }

        with freeze_time("2021-05-23 12:34:56"):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params)

        # 更新処理を実行

        reference_params = {
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
            'quotations_details_set-0-merchandise_description': '商品明細',
            'quotations_details_set-0-quantity': 20,
            'quotations_details_set-0-unit': '単位',
            'quotations_details_set-0-sales_unit_price': -1073741824,
            'quotations_details_set-0-purchase_unit_price': 0,

            'file': ''
        }

        with freeze_time("2021-05-24 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'quotation:reference',
                    kwargs={
                        'pk': registration_params['quotation_id']}),
                reference_params)

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), constant_values.ERR_MESSAGE_0006)
        self.assertEqual(str(messages[2]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        queryset = Quotations.objects.filter(
            pk=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['client_id_id'],
            registration_params['client_id'])
        self.assertEqual(queryset[0]['username_id'], 1)
        self.assertEqual(
            queryset[0]['created_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            queryset[0]['updated_datetime'], datetime(
                2021, 5, 23, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]['expiry'], registration_params['expiry'])
        self.assertEqual(
            queryset[0]['recipient'],
            registration_params['recipient'])
        self.assertEqual(queryset[0]['title'], registration_params['title'])
        self.assertEqual(
            queryset[0]['delivery_time'],
            registration_params['delivery_time'])
        self.assertEqual(
            queryset[0]['delivery_location'],
            registration_params['delivery_location'])
        self.assertEqual(
            queryset[0]['delivery_method'],
            registration_params['delivery_method'])
        self.assertEqual(
            queryset[0]['payment_condition'],
            registration_params['payment_condition'])
        self.assertEqual(queryset[0]['consumption_tax'], 10)
        self.assertEqual(queryset[0]['remark'], registration_params['remark'])
        self.assertTrue(queryset[0]['is_active'])

        queryset = Quotations_details.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(queryset[0]['item_id'], str(
            registration_params['quotation_id']) + '_0')
        self.assertEqual(
            queryset[0]['merchandise'],
            registration_params['quotations_details_set-0-merchandise'])
        self.assertEqual(
            queryset[0]['merchandise_description'],
            registration_params['quotations_details_set-0-merchandise_description'])
        self.assertEqual(
            queryset[0]['quantity'],
            registration_params['quotations_details_set-0-quantity'])
        self.assertEqual(
            queryset[0]['unit'],
            registration_params['quotations_details_set-0-unit'])
        self.assertEqual(
            queryset[0]['sales_unit_price'],
            registration_params['quotations_details_set-0-sales_unit_price'])
        self.assertEqual(
            queryset[0]['purchase_unit_price'],
            registration_params['quotations_details_set-0-purchase_unit_price'])
        self.assertEqual(queryset[0]['order'], 0)
        self.assertTrue(queryset[0]['is_active'])
        self.assertEqual(len(queryset), 1)

# Quotationsモデルの主キー（quotation_id）がAutoFieldのため、採番される値（登録される順番）を明確にする必要あり　そのため、テスト実行順を定義する
# Djangoのテストは「test~」メソッドが実行されるたびにDBが初期化される。Djangoにテストメソッドとして認識されるのは、「test_list_quotation_success_ordering」のみであるため、各々「Test_list_quotation_~」メソッドが完了したあとも、DBの初期化処理は行われない

    def test_update_quotation_ordering(self):
        self.Test_update_quotation_success()
        self.Test_update_quotation_success_max()
        self.Test_update_quotation_success_max_quantity()
        self.Test_update_quotation_success_min()
        self.Test_update_quotation_success_min_integer()
        self.Test_update_quotation_success_min_integer_quantity()
        self.Test_update_quotation_success_FullWidth_integer()
        self.Test_update_quotation_success_special()
        self.Test_update_quotation_success_details_max()
        self.Test_update_quotation_success_max_consumption_tax()
        self.Test_update_quotation_success_min_consumption_tax()
        self.Test_update_quotation_failure_no_Requiredfield()
        self.Test_update_quotation_failure_max()
        self.Test_update_quotation_failure_min_integer()
        self.Test_update_quotation_failure_max_consumption_tax()
        self.Test_update_quotation_failure_min_consumption_tax()
