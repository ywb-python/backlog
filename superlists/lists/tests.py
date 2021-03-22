from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    """
    视图函数home_page的单元测试
    """
    def test_uses_home_template(self):
        """
        测试网站根路径("/")能否被正确解析，映射到对应的视图函数上
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):
    """
    视图函数new_list的单元测试
    """

    def test_can_save_a_POST_request(self):
        """
        测试首页能否处理post请求并成功保存其内容
        """
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        测试首页处理完post请求之后的重定向是否正确
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    """
    视图函数add_item的单元测试
    """

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        测试新生成的待办事项有没有加入到现有的清单中
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
        data={"item_text": "A new item for an existing list"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """
        测试新提交待办事项后重定向的正确性
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
        data={"item_text": "A new item for an existing list"}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')


class ListViewTest(TestCase):
    """
    视图函数view_list的单元测试
    """

    def test_uses_list_template(self):
        """
        测试网站根路径("/lists/{list_.id}/")能否被正确解析，映射到对应的视图函数上
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """
        测试新提交的待办事项是否正确显示在对应的模板上
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        """
        测试是否可以显示对应List对象下的所有待办事项
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


class ListAndItemModelsTest(TestCase):
    """
    模型List和Item的单元测试
    """
    def test_saving_and_retrieving_items(self):
        """
        测试新建List对象名下的待办事项能否被正确保存并显示
        """
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


# Create your tests here.
