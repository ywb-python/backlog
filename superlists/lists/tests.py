from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    """
    视图函数home_page的单元测试
    """
    def test_uses_home_template(self):
        """
        测试网站根路径("/")能否被正确解析，映射到对应的视图函数上
        """
        response = self.client.get('/')
        # assertTemplateUsed():检查响应是使用哪个模板进行渲染的
        self.assertTemplateUsed(response, 'home.html')

    def test_displays_all_list_items(self):
        """
        测试首页是否可以显示多个待办事项
        """
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        response = self.client.get('/')
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_can_save_a_POST_request(self):
        """
        测试首页能否处理post请求并成功保存其内容
        """
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        测试首页处理完post请求之后的重定向是否正确
        """
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        """
        测试首页默认加载的待办事项情形
        """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    """
    待办事项模型Item的单元测试
    """

    def test_saving_and_retrieving_items(self):
        """
        测试多个Item对象是否可以保存成功并且在页面上正确显示
        """
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

# Create your tests here.
