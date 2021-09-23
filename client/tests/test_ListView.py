from paperwork_system.tests.LoggedInTestCase import LoggedInTestCase
from django.urls import reverse_lazy
import freezegun

from ..models import Clients


class Test_ClientListView(LoggedInTestCase):

    # 正常系
    def test_list_client_success(self):

        params = {
            'name': 'あいうえお',
            'name_kana': 'アイウエオ'
        }

        # テスト用データの作成
        client1 = Clients.objects.create(
            name=params['name'],
            name_kana=params['name_kana']
        )

        client2 = Clients.objects.create(
            name='あいueo',
            name_kana='アイｕｅｏ'
        )

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" value="' +
            params["name_kana"] +
            '" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client1.name + '>]>')

        # ページネーションが存在しないことを検証
        self.assertEqual(str(response.context['is_paginated']), 'False')

        # 期待結果以外が表示されていない検証
        self.assertNotEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client2.name + '>]>')

    def test_list_client_success_input_variation_exist_notexist(self):

        # テスト用データの作成
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )

        client2 = Clients.objects.create(
            name='あいueo',
            name_kana='アイｕｅｏ'
        )

        params = {
            'name': 'あいうえお',
            'name_kana': ''
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client1.name + '>]>')

        # 期待結果以外が表示されていない検証
        self.assertNotEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client2.name + '>]>')

    def test_list_client_success_input_variation_notexist_exist(self):

        # テスト用データの作成
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )

        client2 = Clients.objects.create(
            name='あいueo',
            name_kana='アイｕｅｏ'
        )

        params = {
            'name': '',
            'name_kana': 'アイウエオ'
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" value="' +
            params["name_kana"] +
            '" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client1.name + '>]>')

        # 期待結果以外が表示されていない検証
        self.assertNotEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client2.name + '>]>')

    # ソートテストを含める
    def test_list_client_success_input_variation_notexist_notexist(self):

        # テスト用データの作成
        freezer = freezegun.freeze_time('2021-05-24')
        freezer.start()
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-25')
        freezer.start()
        client2 = Clients.objects.create(
            name='あいueo',
            name_kana='アイｕｅｏ'
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-26')
        freezer.start()
        client3 = Clients.objects.create(
            name='1234',
            name_kana='１２３４'
        )
        freezer.stop()

        params = {
            'name': '',
            'name_kana': ''
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Clients: ' +
            client3.name +
            '>, <Clients: ' +
            client2.name +
            '>, <Clients: ' +
            client1.name +
            '>]>')  # 順序は更新日時を降順

    # 部分一致　前方一致も後方一致も部分一致として認識するため　このテストのみで可
    def test_list_client_success_partial_match_name(self):

        # テスト用データの作成
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )

        client2 = Clients.objects.create(
            name='あいueo',
            name_kana='アイｕｅｏ'
        )

        params = {
            'name': 'いう',
            'name_kana': ''
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client1.name + '>]>')

        # 期待結果以外が表示されていない検証
        self.assertNotEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client2.name + '>]>')

    def test_list_client_success_partial_match_name_kana(self):

        # テスト用データの作成
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )

        client2 = Clients.objects.create(
            name='あいueo',
            name_kana='アイｕｅｏ'
        )

        params = {
            'name': '',
            'name_kana': 'イウ'
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(str(
            response.context['search_form']['name']), '<input type="text" name="name" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" value="' +
            params["name_kana"] +
            '" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client1.name + '>]>')

        # 期待結果以外が表示されていない検証
        self.assertNotEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client2.name + '>]>')

    def test_list_client_success_is_active_check(self):

        params = {
            'name': 'あいうえお',
            'name_kana': 'アイウエオ'
        }

        # テスト用データの作成
        client1 = Clients.objects.create(
            name=params['name'],
            name_kana=params['name_kana'],
            is_active=False
        )

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" value="' +
            params["name_kana"] +
            '" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

    def test_list_client_success_andsearch_unmatch_match(self):

        # テスト用データの作成
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )

        params = {
            'name': 'あいうえo',
            'name_kana': 'アイウエオ'
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" value="' +
            params["name_kana"] +
            '" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

    def test_list_client_success_andsearch_match_unmatch(self):

        # テスト用データの作成
        client1 = Clients.objects.create(
            name='あいうえお',
            name_kana='アイウエオ'
        )

        params = {
            'name': 'あいうえお',
            'name_kana': 'アイウエo'
        }

        #検索処理を実行
        response = self.client.post(reverse_lazy('client:list'), params)

        # 検索フォームに検索値が格納されている検証
        self.assertEqual(
            str(
                response.context['search_form']['name']),
            '<input type="text" name="name" value="' +
            params["name"] +
            '" id="id_name">')
        self.assertEqual(
            str(
                response.context['search_form']['name_kana']),
            '<input type="text" name="name_kana" value="' +
            params["name_kana"] +
            '" id="id_name_kana">')

        # 検索結果の正当性を検証
        self.assertEqual(str(response.context['object_list']), '<QuerySet []>')

    def test_list_client_success_pagination(self):

        # テスト用データの作成
        freezer = freezegun.freeze_time('2021-05-24')
        freezer.start()
        client1 = Clients.objects.create(
            name='a',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-25')
        freezer.start()
        client2 = Clients.objects.create(
            name='b',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-26')
        freezer.start()
        client3 = Clients.objects.create(
            name='c',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-27')
        freezer.start()
        client4 = Clients.objects.create(
            name='d',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-28')
        freezer.start()
        client5 = Clients.objects.create(
            name='e',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-29')
        freezer.start()
        client6 = Clients.objects.create(
            name='f',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-30')
        freezer.start()
        client7 = Clients.objects.create(
            name='g',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-05-31')
        freezer.start()
        client8 = Clients.objects.create(
            name='h',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-01')
        freezer.start()
        client9 = Clients.objects.create(
            name='i',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-02')
        freezer.start()
        client10 = Clients.objects.create(
            name='j',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-03')
        freezer.start()
        client11 = Clients.objects.create(
            name='k',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-04')
        freezer.start()
        client12 = Clients.objects.create(
            name='l',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-05')
        freezer.start()
        client13 = Clients.objects.create(
            name='m',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-06')
        freezer.start()
        client14 = Clients.objects.create(
            name='n',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-07')
        freezer.start()
        client15 = Clients.objects.create(
            name='o',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-08')
        freezer.start()
        client16 = Clients.objects.create(
            name='p',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-09')
        freezer.start()
        client17 = Clients.objects.create(
            name='q',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-10')
        freezer.start()
        client18 = Clients.objects.create(
            name='r',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-11')
        freezer.start()
        client19 = Clients.objects.create(
            name='s',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-12')
        freezer.start()
        client20 = Clients.objects.create(
            name='t',
            name_kana=''
        )
        freezer.stop()

        freezer = freezegun.freeze_time('2021-06-13')
        freezer.start()
        client21 = Clients.objects.create(
            name='u',
            name_kana=''
        )
        freezer.stop()

        # ページネーション初期
        response = self.client.get(reverse_lazy('client:list'))

        # 表示結果の正当性を検証
        self.assertEqual(
            str(
                response.context['object_list']),
            '<QuerySet [<Clients: ' +
            client21.name +
            '>, <Clients: ' +
            client20.name +
            '>, <Clients: ' +
            client19.name +
            '>, <Clients: ' +
            client18.name +
            '>, <Clients: ' +
            client17.name +
            '>, <Clients: ' +
            client16.name +
            '>, <Clients: ' +
            client15.name +
            '>, <Clients: ' +
            client14.name +
            '>, <Clients: ' +
            client13.name +
            '>, <Clients: ' +
            client12.name +
            '>, <Clients: ' +
            client11.name +
            '>, <Clients: ' +
            client10.name +
            '>, <Clients: ' +
            client9.name +
            '>, <Clients: ' +
            client8.name +
            '>, <Clients: ' +
            client7.name +
            '>, <Clients: ' +
            client6.name +
            '>, <Clients: ' +
            client5.name +
            '>, <Clients: ' +
            client4.name +
            '>, <Clients: ' +
            client3.name +
            '>, <Clients: ' +
            client2.name +
            '>]>')
        self.assertEqual(str(response.context['page_obj']), '<Page 1 of 2>')
        self.assertEqual(str(response.context['is_paginated']), 'True')

        # ページネーション遷移
        response = self.client.get(reverse_lazy('client:list') + '?page=2')

        # 表示結果の正当性を検証
        self.assertEqual(str(
            response.context['object_list']), '<QuerySet [<Clients: ' + client1.name + '>]>')
        self.assertEqual(str(response.context['page_obj']), '<Page 2 of 2>')
        self.assertEqual(str(response.context['is_paginated']), 'True')
