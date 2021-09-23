from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
from freezegun import freeze_time
from django.core.files.base import ContentFile
import os
from shutil import rmtree
from django.conf import settings

from ..models import Quotations, Quotations_details, Quotations_attached_file, Clients


@freeze_time("2021-05-24 12:34:56")
class Test_QuotationFileDeleteView(LoggedInTestCase):
    # 事前準備
    test_directory_path = settings.MEDIA_ROOT + \
        '\\uploads\\2021\\05\\24\\'.replace('\\\\', '\\')

    if os.path.exists(test_directory_path):
        rmtree(test_directory_path)

# 正常系
    def test_delete_file_success(self):

        # テスト用データの作成
        registration_client = Clients.objects.create(
            client_id=1,
            name='顧客名'
        )

        file_object = ContentFile(b'file content', 'test.txt')

        registration_params = {
            'quotation_id': 1,
            'client_id': registration_client.client_id,
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

        self.client.post(
            reverse_lazy('quotation:registration'),
            registration_params)

        # 登録確認
        queryset = Quotations_attached_file.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(
            queryset[0]['file'],
            'uploads/2021/05/24/' +
            file_object.name)
        self.assertTrue(os.path.exists(self.test_directory_path))

        # ファイル削除処理を実行
        response = self.client.get(
            reverse_lazy(
                'quotation:filedelete', kwargs={
                    'pk': registration_params['quotation_id']}))

        # ファイル削除処理の正当性を検証
        queryset = Quotations_attached_file.objects.filter(
            quotation_id=registration_params['quotation_id']).values()
        self.assertEqual(len(queryset), 0)
        # self.assertFalse(os.path.exists(self.test_directory_path))
        # django-cleanupの動作(実物ファイルの削除)が本テストで確認不可のため、手動テストで確認する

        # 後処理
        os.remove(
            settings.MEDIA_ROOT +
            '\\uploads\\2021\\05\\24\\' +
            file_object.name.replace(
                '\\\\',
                '\\'))
