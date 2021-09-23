from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
import os
from django.conf import settings

from ..models import Quotations, Quotations_details, Quotations_attached_file, Clients


class Test_QuotationExcelDownloadView(LoggedInTestCase):

    # 正常系
    def test_download_excel_success(self):

        # テスト用データの作成
        registration_client = Clients.objects.create(
            client_id=1,
            name='顧客名'
        )

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

            'file': ''
        }

        self.client.post(
            reverse_lazy('quotation:registration'),
            registration_params)

        # Excelダウンロード処理を実行
        response = self.client.get(
            reverse_lazy(
                'quotation:exceldownload', kwargs={
                    'pk': registration_params['quotation_id']}))

        # Excel作成の検証
        self.assertTrue(os.path.exists(settings.BASE_DIR +
                                       '/quotation/lib/quotation_excel/created_excel/' +
                                       'No ' +
                                       str(registration_params['quotation_id']) +
                                       '.xlsx'.replace('/', '\\')))

        # ダウンロードExcelファイルの正当性を検証
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="No ' + str(
                registration_params['quotation_id']) + '.xlsx"')
        self.assertEqual(response['Content-Length'], '8355')
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # 後処理
        response.close()
        os.remove(settings.BASE_DIR +
                  '/quotation/lib/quotation_excel/created_excel/' +
                  'No ' +
                  str(registration_params['quotation_id']) +
                  '.xlsx'.replace('/', '\\'))
