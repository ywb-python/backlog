from django.test import TestCase


class HomePageTest(TestCase):
    """
    视图函数home_page()对应的单元测试用例
    """

    def test_uses_home_template(self):
        """
        测试网站根路径("/")能否被正确解析，映射到对应的视图函数上，并测试所渲染模板的正确性
        """
        response = self.client.get('/')
        # assertTemplateUsed():检查响应是使用哪个模板进行渲染的
        self.assertTemplateUsed(response, 'home.html')

# Create your tests here.
