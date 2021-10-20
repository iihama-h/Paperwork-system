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


@freeze_time("2021-05-24 12:34:56")
class Test_QuotationDeleteView(LoggedInTestCase):
    # 事前準備
    test_directory_path = settings.MEDIA_ROOT + \
        '\\uploads\\2021\\05\\24\\'.replace('\\\\', '\\')

    if os.path.exists(test_directory_path):
        rmtree(test_directory_path)

# 正常系
    def test_delete_quotation_success(self):

        # テスト用データの作成
        registration_client = Clients.objects.create(
            client_id=1,
            name='顧客名'
        )

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

        self.client.post(reverse_lazy('quotation:registration'), params)

        # 登録確認
        self.assertEqual(
            len((Quotations.objects.filter(pk=params['quotation_id']).values())), 1)
        self.assertEqual(len((Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values())), 1)
        self.assertEqual(len((Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).values())), 1)
        self.assertTrue(os.path.exists(self.test_directory_path))

        # 削除処理を実行
        response = self.client.post(
            reverse_lazy(
                'quotation:delete', kwargs={
                    'pk': params['quotation_id']}))

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('quotation:list'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), constant_values.MESSAGE_0003)

        # 物理削除されたことを検証
        self.assertEqual(
            len((Quotations.objects.filter(pk=params['quotation_id']).values())), 0)
        self.assertEqual(len((Quotations_details.objects.filter(
            quotation_id=params['quotation_id']).values())), 0)
        self.assertEqual(len((Quotations_attached_file.objects.filter(
            quotation_id=params['quotation_id']).values())), 0)
        # self.assertFalse(os.path.exists(self.test_directory_path))
        # django-cleanupの動作(実物ファイルの削除)が本テストで確認不可のため、手動テストで確認する

        # 後処理
        rmtree(
            settings.MEDIA_ROOT +
            '\\uploads\\2021\\05\\24\\'.replace(
                '\\\\',
                '\\'))


# 異常系

    def test_delete_quotation_failure_nothing_pk(self):

        # 存在しないPKで削除処理を実行
        response = self.client.post(
            reverse_lazy(
                'quotation:delete',
                kwargs={
                    'pk': 999}))

        # エラーになることを検証
        self.assertEqual(response.status_code, 404)
