from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
from datetime import datetime
from django.utils import timezone
from freezegun import freeze_time
from django.contrib.messages import get_messages

from ..models import Clients


class Test_ClientRegistrationView(
        LoggedInTestCase):
    # 正常系
    @freeze_time("2021-05-24 12:34:56")
    def test_create_client_success(self):
        params = {
            "name": "顧客名",
            "name_kana": "フリガナ",
            "department": "部署",
            "industry": "業種",
            "capital": 1111,
            "postcode": "123-0000",
            "address": "住所",
            "phone_number": "111111111",
            "email": "email@address.com",
            "fax_number": "22222222222",
            "revenue": 22222,
            "profit": 333333,
            "number_of_employees": 4444444,
            "remark": "aeiuo"
        }

        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録が完了しました。')

        # DBへの登録を検証
        self.assertEqual(Clients.objects.filter(name='顧客名').count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Clients.objects.filter(name='顧客名').values()
        self.assertIsNotNone(queryset[0]["client_id"])
        self.assertEqual(queryset[0]["name"], params["name"])
        self.assertEqual(queryset[0]["name_kana"], params["name_kana"])
        self.assertEqual(queryset[0]["department"], params["department"])
        self.assertEqual(queryset[0]["industry"], params["industry"])
        self.assertEqual(queryset[0]["capital"], params["capital"])
        self.assertEqual(queryset[0]["postcode"], params["postcode"])
        self.assertEqual(queryset[0]["address"], params["address"])
        self.assertEqual(queryset[0]["phone_number"], params["phone_number"])
        self.assertEqual(queryset[0]["email"], params["email"])
        self.assertEqual(queryset[0]["fax_number"], params["fax_number"])
        self.assertEqual(
            queryset[0]["updated_datetime"], datetime(
                2021, 5, 24, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]["revenue"], params["revenue"])
        self.assertEqual(queryset[0]["profit"], params["profit"])
        self.assertEqual(
            queryset[0]["number_of_employees"],
            params["number_of_employees"])
        self.assertEqual(queryset[0]["remark"], params["remark"])
        self.assertTrue(queryset[0]["is_active"])

    def test_create_client_success_max(self):
        params = {
            "name": "顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名",
            "name_kana": "フリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガナフリガ",
            "department": "部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部署部",
            "industry": "業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業種業業種",
            "capital": 2147483647,
            "postcode": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            "address": "住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住所住",
            "phone_number": "222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",
            "fax_number": "333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333",
            "revenue": 2147483647,
            "profit": 2147483647,
            "number_of_employees": 2147483647,
        }

        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録が完了しました。')

        # DBへの登録を検証
        self.assertEqual(
            Clients.objects.filter(
                name='顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名').count(),
            1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Clients.objects.filter(
            name='顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名').values()
        self.assertIsNotNone(queryset[0]["client_id"])
        self.assertEqual(queryset[0]["name"], params["name"])
        self.assertEqual(queryset[0]["name_kana"], params["name_kana"])
        self.assertEqual(queryset[0]["department"], params["department"])
        self.assertEqual(queryset[0]["industry"], params["industry"])
        self.assertEqual(queryset[0]["capital"], params["capital"])
        self.assertEqual(queryset[0]["postcode"], params["postcode"])
        self.assertEqual(queryset[0]["address"], params["address"])
        self.assertEqual(queryset[0]["phone_number"], params["phone_number"])
        self.assertEqual(queryset[0]["fax_number"], params["fax_number"])
        self.assertEqual(queryset[0]["revenue"], params["revenue"])
        self.assertEqual(queryset[0]["profit"], params["profit"])
        self.assertEqual(
            queryset[0]["number_of_employees"],
            params["number_of_employees"])

    @freeze_time("2020-02-29 12:34:56")
    def test_create_client_success_min(self):
        params = {
            "name": "a",
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

        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録が完了しました。')

        # DBへの登録を検証
        self.assertEqual(Clients.objects.filter(name='a').count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Clients.objects.filter(name='a').values()
        self.assertIsNotNone(queryset[0]["client_id"])
        self.assertEqual(queryset[0]["name"], params["name"])
        self.assertIsNone(queryset[0]["name_kana"])
        self.assertIsNone(queryset[0]["department"])
        self.assertIsNone(queryset[0]["industry"])
        self.assertIsNone(queryset[0]["capital"])
        self.assertIsNone(queryset[0]["postcode"])
        self.assertIsNone(queryset[0]["address"])
        self.assertIsNone(queryset[0]["phone_number"])
        self.assertIsNone(queryset[0]["email"])
        self.assertIsNone(queryset[0]["fax_number"])
        self.assertEqual(
            queryset[0]["updated_datetime"], datetime(
                2020, 2, 29, 12, 34, 56, tzinfo=timezone.utc))
        self.assertIsNone(queryset[0]["revenue"])
        self.assertIsNone(queryset[0]["profit"])
        self.assertIsNone(queryset[0]["number_of_employees"])
        self.assertEqual(queryset[0]["remark"], params["remark"])
        self.assertTrue(queryset[0]["is_active"])

    def test_create_client_success_min_integer(self):
        params = {
            "name": "b",
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

        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録が完了しました。')

        # DBへの登録を検証
        self.assertEqual(Clients.objects.filter(name='b').count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Clients.objects.filter(name='b').values()
        self.assertEqual(queryset[0]["capital"], params["capital"])
        self.assertEqual(queryset[0]["revenue"], params["revenue"])
        self.assertEqual(queryset[0]["profit"], params["profit"])
        self.assertEqual(
            queryset[0]["number_of_employees"],
            params["number_of_employees"])

    def test_create_client_success_FullWidth_integer(self):
        params = {
            "name": "b",
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

        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録が完了しました。')

        # DBへの登録を検証
        self.assertEqual(Clients.objects.filter(name='b').count(), 1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Clients.objects.filter(name='b').values()
        self.assertEqual(queryset[0]["capital"], 2147483647)
        self.assertEqual(queryset[0]["revenue"], 2147483647)
        self.assertEqual(queryset[0]["profit"], 2147483647)
        self.assertEqual(queryset[0]["number_of_employees"], 2147483647)

    @freeze_time("2020-02-29 12:34:56")
    def test_create_client_success_special(self):
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

        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:registration'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録が完了しました。')

        # DBへの登録を検証
        self.assertEqual(
            Clients.objects.filter(
                name="aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>").count(),
            1)

        # 各フィールドに登録されている値の正当性を検証
        queryset = Clients.objects.filter(
            name="aAａＡあアｱ阿濵1１𠥼,./\\]:;@[^-!\"#$%&'()=~|{`+*}_?>< 　<h1>HTML</h1>").values()
        self.assertIsNotNone(queryset[0]["client_id"])
        self.assertEqual(queryset[0]["name"], params["name"])
        self.assertEqual(queryset[0]["name_kana"], params["name_kana"])
        self.assertEqual(queryset[0]["department"], params["department"])
        self.assertEqual(queryset[0]["industry"], params["industry"])
        self.assertEqual(queryset[0]["postcode"], params["postcode"])
        self.assertEqual(queryset[0]["address"], params["address"])
        self.assertEqual(queryset[0]["phone_number"], params["phone_number"])
        self.assertEqual(queryset[0]["fax_number"], params["fax_number"])
        self.assertEqual(
            queryset[0]["updated_datetime"], datetime(
                2020, 2, 29, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(queryset[0]["remark"], params["remark"])
        self.assertTrue(queryset[0]["is_active"])


# 異常系


    def test_create_client_failure_No_Requiredfield(self):
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
        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'name', 'このフィールドは必須です。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録ができませんでした。')

        # DBに登録されていないことを検証
        self.assertNotEqual(Clients.objects.filter(name='').count(), 1)

    def test_create_client_failure_MAX(self):
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
        response = self.client.post(
            reverse_lazy('client:registration'), params)

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
        self.assertEqual(str(messages[0]), '登録ができませんでした。')

        # DBに登録されていないことを検証
        self.assertNotEqual(
            Clients.objects.filter(
                name='顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧客名顧').count(),
            1)

    def test_create_client_failure_min_integer(self):
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
        response = self.client.post(
            reverse_lazy('client:registration'), params)

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
        self.assertEqual(str(messages[0]), '登録ができませんでした。')

        # DBに登録されていないことを検証
        self.assertNotEqual(Clients.objects.filter(name='c').count(), 1)

    def test_create_client_failure_No_integer(self):
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
        response = self.client.post(
            reverse_lazy('client:registration'), params)

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
        self.assertEqual(str(messages[0]), '登録ができませんでした。')

        # DBに登録されていないことを検証
        self.assertNotEqual(Clients.objects.filter(name='d').count(), 1)

    def test_create_client_failure_FloatField(self):
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
        response = self.client.post(
            reverse_lazy('client:registration'), params)

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
        self.assertEqual(str(messages[0]), '登録ができませんでした。')

        # DBに登録されていないことを検証
        self.assertNotEqual(Clients.objects.filter(name='e').count(), 1)

    def test_create_client_failure_No_email(self):
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
        response = self.client.post(
            reverse_lazy('client:registration'), params)

        # フォームフィールドの異常値によりエラーになることを検証
        self.assertFormError(response, 'form', 'email', '有効なメールアドレスを入力してください。')

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '登録ができませんでした。')

        # DBに登録されていないことを検証
        self.assertNotEqual(Clients.objects.filter(name='f').count(), 1)
