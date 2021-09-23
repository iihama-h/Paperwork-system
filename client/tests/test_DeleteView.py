from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
from django.contrib.messages import get_messages

from ..models import Clients


class Test_ClientDeleteView(LoggedInTestCase):
    # 正常系
    def test_delete_client_success(self):

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

        # 登録時はis_activeがTrueであることを検証
        self.assertTrue(Clients.objects.get(pk=client.pk).is_active)

        # 削除処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:delete', kwargs={
                    'pk': client.pk}))

        # リダイレクトを検証
        self.assertRedirects(response, reverse_lazy('client:list'))

        # メッセージを検証
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '削除が完了しました。')

        # 論理削除されたことを検証
        self.assertFalse(Clients.objects.get(pk=client.pk).is_active)


# 異常系


    def test_delete_client_failure_nothing_pk(self):

        # 存在しないPKで削除処理を実行
        response = self.client.post(
            reverse_lazy(
                'client:delete', kwargs={
                    'pk': 999}))

        # エラーになることを検証
        self.assertEqual(response.status_code, 404)
