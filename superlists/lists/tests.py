from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        """
        测试网站根路径("/")能否被正确解析，映射到对应的视图函数上
        """
        # resolve():解析url，并将其映射到对应的视图函数上
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        测试视图函数home_page()返回内容的正确性
        """
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))


# Create your tests here.
