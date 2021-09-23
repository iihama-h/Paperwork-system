from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
from django.utils import timezone
from freezegun import freeze_time
from django.contrib.auth import get_user_model

from ..models import Quotations, Quotations_details, Quotations_attached_file, Clients


class Test_QuotationListView(LoggedInTestCase):

    def setup(self):
        # テスト用データの作成
        # quotation_id 1の登録
        registration_client1 = Clients.objects.create(
            client_id=1,
            name='顧客名1'
        )

        registration_params1 = {
            'quotation_id': 1,
            'client_id': registration_client1.client_id,
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

        with freeze_time('2021-05-24'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params1)

        # quotation_id 2の登録
        registration_client2 = Clients.objects.create(
            client_id=2,
            name='顧客名2'
        )

        registration_params2 = {
            'quotation_id': 2,
            'client_id': registration_client2.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': 'title',
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

        with freeze_time('2021-05-25'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params2)

        # quotation_id 3の登録
        self.client.logout()

        self.id = 2
        self.username = 'testes_user'
        self.email = 'test@test.com'
        self.password = 'password'

        self.test_user = get_user_model().objects.create_user(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password)

        self.client.login(username=self.username, password=self.password)

        registration_client3 = Clients.objects.create(
            client_id=3,
            name='顧客名3'
        )

        registration_params3 = {
            'quotation_id': 3,
            'client_id': registration_client3.client_id,
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

        with freeze_time('2021-05-26'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params3)

        # DBへの登録を検証
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=registration_params1['quotation_id']).count(), 1)
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=registration_params2['quotation_id']).count(), 1)
        self.assertEqual(
            Quotations.objects.filter(
                quotation_id=registration_params3['quotation_id']).count(), 1)


# 正常系

    def Test_list_quotation_success(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': 'test_user',
            'updated_datetime': '2021-05-24',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_all_notexist(self):  # ソートテストを含める

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': '',
            'updated_datetime': '',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Quotations: ' +
            '3' +
            '>, <Quotations: ' +
            '2' +
            '>, <Quotations: ' +
            '1' +
            '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    # ennn exist_notexist_notexist_notexistの略
    def Test_list_quotation_success_input_variation_ennn(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': '',
            'updated_datetime': '',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_nenn(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': 'test_user',
            'updated_datetime': '',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Quotations: ' +
            '2' +
            '>, <Quotations: ' +
            '1' +
            '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_nnen(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': '',
            'updated_datetime': '2021-05-24',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_nnne(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': '',
            'updated_datetime': '',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Quotations: ' +
            '3' +
            '>, <Quotations: ' +
            '1' +
            '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_eenn(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': 'test_user',
            'updated_datetime': '',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_enen(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': '',
            'updated_datetime': '2021-05-24',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_enne(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': '',
            'updated_datetime': '',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_neen(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': 'test_user',
            'updated_datetime': '2021-05-24',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_nene(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': 'test_user',
            'updated_datetime': '',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_input_variation_nnee(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': '',
            'updated_datetime': '2021-05-24',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    # 部分一致　前方一致も後方一致も部分一致として認識するため　このテストのみで可
    def Test_list_quotation_success_partial_match_name(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '客名',
            'username': '',
            'updated_datetime': '',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Quotations: ' +
            '3' +
            '>, <Quotations: ' +
            '2' +
            '>, <Quotations: ' +
            '1' +
            '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_partial_match_username(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': 'st_us',
            'updated_datetime': '',
            'title': ''
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Quotations: ' +
            '2' +
            '>, <Quotations: ' +
            '1' +
            '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_partial_match_title(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '',
            'username': '',
            'updated_datetime': '',
            'title': 'it'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '2' + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_andsearch_name_unmatch(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名A',
            'username': 'test_user',
            'updated_datetime': '2021-05-24',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_andsearch_username_unmatch(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': 'test_users',
            'updated_datetime': '2021-05-24',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_andsearch_updated_datetime_unmatch(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': 'test_user',
            'updated_datetime': '2020-05-24',
            'title': '件名'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_andsearch_updated_title_unmatch(self):

        #検索処理を実行 (Viewクラス)
        params = {
            'name': '顧客名1',
            'username': 'test_user',
            'updated_datetime': '2020-05-24',
            'title': 'タイトル'
        }

        response = self.client.post(reverse_lazy('quotation:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['username']),
            '<input type="text" name="username" value="' +
            params["username"] +
            '" id="id_username">')
        # self.assertEqual(str(response.context['search_form']['updated_datetime']),
        # '') input形式がbootstrap_datepicker_plusにより特殊なため、ユニットテストでは確認を行わない
        self.assertEqual(
            str(
                response.context['search_form']['title']),
            '<input type="text" name="title" value="' +
            params["title"] +
            '" id="id_title">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

    def Test_list_quotation_success_pagination(self):

        registration_client4 = Clients.objects.create(
            client_id=4,
            name='顧客名4'
        )

        registration_params4 = {
            'quotation_id': 4,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-05-27'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params4)

        registration_params5 = {
            'quotation_id': 5,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-05-28'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params5)

        registration_params6 = {
            'quotation_id': 6,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-05-29'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params6)

        registration_params7 = {
            'quotation_id': 7,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-05-30'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params7)

        registration_params8 = {
            'quotation_id': 8,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-05-31'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params8)

        registration_params9 = {
            'quotation_id': 9,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-01'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params9)

        registration_params10 = {
            'quotation_id': 10,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-02'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params10)

        registration_params11 = {
            'quotation_id': 11,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-03'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params11)

        registration_params12 = {
            'quotation_id': 12,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-04'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params12)

        registration_params13 = {
            'quotation_id': 13,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-05'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params13)

        registration_params14 = {
            'quotation_id': 14,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-06'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params14)

        registration_params15 = {
            'quotation_id': 15,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-07'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params15)

        registration_params16 = {
            'quotation_id': 16,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-08'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params16)

        registration_params17 = {
            'quotation_id': 17,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-09'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params17)

        registration_params18 = {
            'quotation_id': 18,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-10'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params18)

        registration_params19 = {
            'quotation_id': 19,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-11'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params19)

        registration_params20 = {
            'quotation_id': 20,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-12'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params20)

        registration_params21 = {
            'quotation_id': 21,
            'client_id': registration_client4.client_id,
            'expiry': '見積有効期限',
            'recipient': '宛名',
            'title': '件名',
            'delivery_time': '納期',
            'delivery_location': '納入場所',
            'delivery_method': '納入方法',
            'payment_condition': '取引条件',
            'remark': '備考',

            'quotations_details_set-TOTAL_FORMS': 0,
            'quotations_details_set-INITIAL_FORMS': 0,
            'quotations_details_set-MIN_NUM_FORMS': 0,
            'quotations_details_set-MAX_NUM_FORMS': 1000,

            'file': ''
        }

        with freeze_time('2021-06-13'):
            self.client.post(
                reverse_lazy('quotation:registration'),
                registration_params21)

        # self.id = 2
        # self.username = 'testes_user'
        # self.email = 'test@test.com'
        # self.password = 'password'
        #
        # self.test_user = get_user_model().objects.create_user(
        #     id=self.id,
        #     username=self.username,
        #     email=self.email,
        #     password=self.password)
        #
        # self.client.login(username=self.username, password=self.password)

        # ページネーション初期
        response = self.client.get(reverse_lazy('quotation:list'))

        # ページネーションが存在することを検証
        self.assertEqual(str(response.context['is_paginated']), 'True')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet [<Quotations: 21>, <Quotations: 20>, <Quotations: 19>, <Quotations: 18>, <Quotations: 17>, <Quotations: 16>, <Quotations: 15>, <Quotations: 14>, <Quotations: 13>, <Quotations: 12>, <Quotations: 11>, <Quotations: 10>, <Quotations: 9>, <Quotations: 8>, <Quotations: 7>, <Quotations: 6>, <Quotations: 5>, <Quotations: 4>, <Quotations: 3>, <Quotations: 2>]>')
        self.assertEqual(str(response.context['page_obj']), '<Page 1 of 2>')

        # ページネーション遷移
        response = self.client.get(reverse_lazy('quotation:list') + '?page=2')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(response.context['object_list']), '<QuerySet [<Quotations: ' + '1' + '>]>')
        self.assertEqual(str(response.context['page_obj']), '<Page 2 of 2>')


# Quotationsモデルの主キー（quotation_id）がAutoFieldのため、採番される値（登録される順番）を明確にする必要あり　そのため、テスト実行順を定義する
# Djangoのテストは「test~」メソッドが実行されるたびにDBが初期化される。Djangoにテストメソッドとして認識されるのは、「test_list_quotation_success_ordering」のみであるため、各々「Test_list_quotation_~」メソッドが完了したあとも、DBの初期化処理は行われない

    def test_list_quotation_ordering(self):
        self.setup()
        self.Test_list_quotation_success()
        self.Test_list_quotation_success_all_notexist()
        self.Test_list_quotation_success_input_variation_ennn()
        self.Test_list_quotation_success_input_variation_nenn()
        self.Test_list_quotation_success_input_variation_nnen()
        self.Test_list_quotation_success_input_variation_nnne()
        self.Test_list_quotation_success_input_variation_eenn()
        self.Test_list_quotation_success_input_variation_enen()
        self.Test_list_quotation_success_input_variation_enne()
        self.Test_list_quotation_success_input_variation_neen()
        self.Test_list_quotation_success_input_variation_nene()
        self.Test_list_quotation_success_input_variation_nnee()
        self.Test_list_quotation_success_partial_match_name()
        self.Test_list_quotation_success_partial_match_username()
        self.Test_list_quotation_success_partial_match_title()
        self.Test_list_quotation_success_andsearch_name_unmatch()
        self.Test_list_quotation_success_andsearch_username_unmatch()
        self.Test_list_quotation_success_andsearch_updated_datetime_unmatch()
        self.Test_list_quotation_success_andsearch_updated_title_unmatch()
        self.Test_list_quotation_success_pagination()
