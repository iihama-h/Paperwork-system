from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
from datetime import datetime
from django.utils import timezone
from freezegun import freeze_time
from django.contrib.messages import get_messages
from paperwork_system import constant_values

from ..models import Clients


class Test_ClientReferenceView(LoggedInTestCase):
    # 正常系
    @freeze_time("2021-05-24 12:34:56")
    def test_update_client_success(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "顧客名変更",
            "name_kana": "フリガナ変更",
            "department": "部署変更",
            "industry": "業種変更",
            "capital": 0000,
            "postcode": "123-0000変更",
            "address": "住所変更",
            "phone_number": "111111111変更",
            "email": "emailchange@address.com",
            "fax_number": "22222222222変更",
            "revenue": 11111,
            "profit": 222222,
            "number_of_employees": 3333333,
            "remark": "aeiuo変更"
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'client:reference', kwargs={
                    'pk': client.pk}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name,
            params["name"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name_kana,
            params["name_kana"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).department,
            params["department"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).industry,
            params["industry"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).capital,
            params["capital"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            params["postcode"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).address,
            params["address"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            params["phone_number"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            params["email"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            params["fax_number"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).updated_datetime, datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).revenue,
            params["revenue"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).profit,
            params["profit"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            params["number_of_employees"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).remark,
            params["remark"])
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_success_max(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧変更",
            "name_kana": "フリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフ変更",
            "department": "部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部変更",
            "industry": "業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業変更",
            "capital": 2147483647,
            "postcode": "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111変更",
            "address": "住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住変更",
            "phone_number": "2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222変更",
            "fax_number": "3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333変更",
            "revenue": 2147483647,
            "profit": 2147483647,
            "number_of_employees": 2147483647,
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'client:reference', kwargs={
                    'pk': client.pk}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name,
            params["name"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name_kana,
            params["name_kana"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).department,
            params["department"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).industry,
            params["industry"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).capital,
            params["capital"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            params["postcode"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).address,
            params["address"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            params["phone_number"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            params["fax_number"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).revenue,
            params["revenue"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).profit,
            params["profit"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            params["number_of_employees"])
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_success_min(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "g",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": "",
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": "",
            "profit": "",
            "number_of_employees": "",
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'client:reference', kwargs={
                    'pk': client.pk}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name,
            params["name"])
        self.assertIsNone(Clients.objects.get(pk=client.pk).name_kana)
        self.assertIsNone(Clients.objects.get(pk=client.pk).department)
        self.assertIsNone(Clients.objects.get(pk=client.pk).industry)
        self.assertIsNone(Clients.objects.get(pk=client.pk).capital)
        self.assertIsNone(Clients.objects.get(pk=client.pk).postcode)
        self.assertIsNone(Clients.objects.get(pk=client.pk).address)
        self.assertIsNone(Clients.objects.get(pk=client.pk).phone_number)
        self.assertIsNone(Clients.objects.get(pk=client.pk).fax_number)
        self.assertIsNone(Clients.objects.get(pk=client.pk).revenue)
        self.assertIsNone(Clients.objects.get(pk=client.pk).profit)
        self.assertIsNone(
            Clients.objects.get(
                pk=client.pk).number_of_employees)
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_success_min_integer(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "h",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": -2147483648,
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": -2147483648,
            "profit": -2147483648,
            "number_of_employees": -2147483648,
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'client:reference', kwargs={
                    'pk': client.pk}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).capital,
            params["capital"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).revenue,
            params["revenue"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).profit,
            params["profit"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            params["number_of_employees"])

    def test_update_client_success_FullWidth_integer(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "i",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": "２１４７４８３６４７",
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": "２１４７４８３６４７",
            "profit": "２１４７４８３６４７",
            "number_of_employees": "２１４７４８３６４７",
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'client:reference', kwargs={
                    'pk': client.pk}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 2147483647)
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 2147483647)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 2147483647)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            2147483647)

    @freeze_time("2021-05-24 12:34:56")
    def test_update_client_success_special(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            remark='aeiuo'
        )

        params = {
            "name": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "name_kana": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "department": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "industry": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "postcode": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "address": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "phone_number": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "fax_number": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>",
            "remark": "aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>"
        }

        # 更新処理を実行
        with freeze_time("2020-02-29 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'client:reference', kwargs={
                        'pk': client.pk}), params)

        # リダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy(
                'client:reference', kwargs={
                    'pk': client.pk}))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.MESSAGE_0002)

        # 各フィールドに変更されている値の正当性を検証
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name,
            params["name"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).name_kana,
            params["name_kana"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).department,
            params["department"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).industry,
            params["industry"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            params["postcode"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).address,
            params["address"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            params["phone_number"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            params["fax_number"])
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).updated_datetime, datetime(
                2020, 2, 29, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).remark,
            params["remark"])
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)


# 異常系

    def test_update_client_failure_nothing_pk(self):

        # 存在しないPKで削除処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': 999}))

        # エラーになることを検証
        self.assertEqual(response.status_code, 404)

    @freeze_time("2021-05-24 12:34:56")
    def test_update_client_failure_No_Requiredfield(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": "",
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": "",
            "profit": "",
            "number_of_employees": "",
            "remark": ""
        }

        # 更新処理を実行
        with freeze_time("2021-05-25 12:34:56"):
            response = self.client.post(
                reverse_lazy(
                    'client:reference', kwargs={
                        'pk': client.pk}), params)

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'name', 'このフィールドは必須です。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        self.assertEqual(Clients.objects.get(pk=client.pk).name, '顧客名')
        self.assertEqual(Clients.objects.get(pk=client.pk).name_kana, 'フリガナ')
        self.assertEqual(Clients.objects.get(pk=client.pk).department, '部署')
        self.assertEqual(Clients.objects.get(pk=client.pk).industry, '業種')
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 1111)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            '123-0000')
        self.assertEqual(Clients.objects.get(pk=client.pk).address, '住所')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            '111111111')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            'email@address.com')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            '22222222222')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).updated_datetime, datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 22222)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 333333)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            4444444)
        self.assertEqual(Clients.objects.get(pk=client.pk).remark, 'aeiuo')
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_failure_max(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧",
            "name_kana": "フリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナ",
            "department": "部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署",
            "industry": "業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種",
            "capital": 2147483648,
            "postcode": "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            "address": "住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所",
            "phone_number": "2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",
            "fax_number": "3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333",
            "revenue": 2147483648,
            "profit": 2147483648,
            "number_of_employees": 2147483648,
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(
            response,
            'form',
            'name',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'name_kana',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'department',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'industry',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'capital',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormError(
            response,
            'form',
            'postcode',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'address',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'phone_number',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'fax_number',
            'この値は 255 文字以下でなければなりません( 256 文字になっています)。')
        self.assertFormError(
            response,
            'form',
            'revenue',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormError(
            response,
            'form',
            'profit',
            'この値は 2147483647 以下でなければなりません。')
        self.assertFormError(
            response,
            'form',
            'number_of_employees',
            'この値は 2147483647 以下でなければなりません。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        self.assertEqual(Clients.objects.get(pk=client.pk).name, '顧客名')
        self.assertEqual(Clients.objects.get(pk=client.pk).name_kana, 'フリガナ')
        self.assertEqual(Clients.objects.get(pk=client.pk).department, '部署')
        self.assertEqual(Clients.objects.get(pk=client.pk).industry, '業種')
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 1111)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            '123-0000')
        self.assertEqual(Clients.objects.get(pk=client.pk).address, '住所')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            '111111111')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            'email@address.com')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            '22222222222')
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 22222)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 333333)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            4444444)
        self.assertEqual(Clients.objects.get(pk=client.pk).remark, 'aeiuo')
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_failure_min_integer(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "c",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": -2147483649,
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": -2147483649,
            "profit": -2147483649,
            "number_of_employees": -2147483649,
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(
            response,
            'form',
            'capital',
            'この値は -2147483648 以上でなければなりません。')
        self.assertFormError(
            response,
            'form',
            'revenue',
            'この値は -2147483648 以上でなければなりません。')
        self.assertFormError(
            response,
            'form',
            'profit',
            'この値は -2147483648 以上でなければなりません。')
        self.assertFormError(
            response,
            'form',
            'number_of_employees',
            'この値は -2147483648 以上でなければなりません。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        self.assertEqual(Clients.objects.get(pk=client.pk).name, '顧客名')
        self.assertEqual(Clients.objects.get(pk=client.pk).name_kana, 'フリガナ')
        self.assertEqual(Clients.objects.get(pk=client.pk).department, '部署')
        self.assertEqual(Clients.objects.get(pk=client.pk).industry, '業種')
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 1111)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            '123-0000')
        self.assertEqual(Clients.objects.get(pk=client.pk).address, '住所')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            '111111111')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            'email@address.com')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            '22222222222')
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 22222)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 333333)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            4444444)
        self.assertEqual(Clients.objects.get(pk=client.pk).remark, 'aeiuo')
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_failure_No_integer(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "d",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": "資本金",
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": "売上高",
            "profit": '利益',
            "number_of_employees": "従業員数",
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(response, 'form', 'capital', '整数を入力してください。')
        self.assertFormError(response, 'form', 'revenue', '整数を入力してください。')
        self.assertFormError(response, 'form', 'profit', '整数を入力してください。')
        self.assertFormError(
            response,
            'form',
            'number_of_employees',
            '整数を入力してください。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        self.assertEqual(Clients.objects.get(pk=client.pk).name, '顧客名')
        self.assertEqual(Clients.objects.get(pk=client.pk).name_kana, 'フリガナ')
        self.assertEqual(Clients.objects.get(pk=client.pk).department, '部署')
        self.assertEqual(Clients.objects.get(pk=client.pk).industry, '業種')
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 1111)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            '123-0000')
        self.assertEqual(Clients.objects.get(pk=client.pk).address, '住所')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            '111111111')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            'email@address.com')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            '22222222222')
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 22222)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 333333)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            4444444)
        self.assertEqual(Clients.objects.get(pk=client.pk).remark, 'aeiuo')
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_failure_FloatField(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "e",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": 0.1,
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "",
            "fax_number": "",
            "revenue": 0.2,
            "profit": 0.3,
            "number_of_employees": 0.4,
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(response, 'form', 'capital', '整数を入力してください。')
        self.assertFormError(response, 'form', 'revenue', '整数を入力してください。')
        self.assertFormError(response, 'form', 'profit', '整数を入力してください。')
        self.assertFormError(
            response,
            'form',
            'number_of_employees',
            '整数を入力してください。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        self.assertEqual(Clients.objects.get(pk=client.pk).name, '顧客名')
        self.assertEqual(Clients.objects.get(pk=client.pk).name_kana, 'フリガナ')
        self.assertEqual(Clients.objects.get(pk=client.pk).department, '部署')
        self.assertEqual(Clients.objects.get(pk=client.pk).industry, '業種')
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 1111)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            '123-0000')
        self.assertEqual(Clients.objects.get(pk=client.pk).address, '住所')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            '111111111')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            'email@address.com')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            '22222222222')
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 22222)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 333333)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            4444444)
        self.assertEqual(Clients.objects.get(pk=client.pk).remark, 'aeiuo')
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

    def test_update_client_failure_No_email(self):

        # テスト用データの作成
        client = Clients.objects.create(
            name='顧客名',
            name_kana='フリガナ',
            department='部署',
            industry='業種',
            capital=1111,
            postcode='123-0000',
            address='住所',
            phone_number='111111111',
            email='email@address.com',
            fax_number='22222222222',
            revenue=22222,
            profit=333333,
            number_of_employees=4444444,
            remark='aeiuo'
        )

        params = {
            "name": "f",
            "name_kana": "",
            "department": "",
            "industry": "",
            "capital": "",
            "postcode": "",
            "address": "",
            "phone_number": "",
            "email": "email",
            "fax_number": "",
            "revenue": "",
            "profit": "",
            "number_of_employees": "",
            "remark": ""
        }

        # 更新処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:reference',
                kwargs={
                    'pk': client.pk}),
            params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(response, 'form', 'email', '有効なメールアドレスを入力してください。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), constant_values.ERR_MESSAGE_0002)

        # 更新されていないことを検証
        self.assertEqual(Clients.objects.get(pk=client.pk).name, '顧客名')
        self.assertEqual(Clients.objects.get(pk=client.pk).name_kana, 'フリガナ')
        self.assertEqual(Clients.objects.get(pk=client.pk).department, '部署')
        self.assertEqual(Clients.objects.get(pk=client.pk).industry, '業種')
        self.assertEqual(Clients.objects.get(pk=client.pk).capital, 1111)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).postcode,
            '123-0000')
        self.assertEqual(Clients.objects.get(pk=client.pk).address, '住所')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).phone_number,
            '111111111')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).email,
            'email@address.com')
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).fax_number,
            '22222222222')
        self.assertEqual(Clients.objects.get(pk=client.pk).revenue, 22222)
        self.assertEqual(Clients.objects.get(pk=client.pk).profit, 333333)
        self.assertEqual(
            Clients.objects.get(
                pk=client.pk).number_of_employees,
            4444444)
        self.assertEqual(Clients.objects.get(pk=client.pk).remark, 'aeiuo')
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)
